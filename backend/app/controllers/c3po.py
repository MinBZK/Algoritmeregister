import requests
from fastapi import HTTPException, status
from app.controllers import collect_structure_data, get_ttl_hash
from app.schemas import (
    C3poRequest,
    User,
    ProcessingRequest,
    C3poResults,
    RuleSetOut,
    Rule,
    ProcessingRequestOut,
)
from functools import lru_cache
from app.config.settings import Settings
import time
from app.util.logger import get_logger
from app.util.html import strip_html

logger = get_logger(__name__)
env_settings = Settings()


def get_c3po(url: str) -> requests.Response:
    try:
        response = requests.request("get", url)

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"C3PO_REQUEST_FAILED: {response.status_code}",
            )
        return response
    except requests.ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="C3PO_CONN_ERROR",
        )


def post_c3po_request(data: ProcessingRequestOut) -> requests.Response:
    try:
        post_response = requests.post(
            f"{env_settings.c3po_url}/processing-request/", json=data
        )

        if post_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"C3PO_REQUEST_FAILED: {post_response.status_code}",
            )
        return post_response
    except requests.ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="C3PO_CONN_ERROR",
        )


@lru_cache(maxsize=1)
def get_version_rules() -> list[RuleSetOut]:
    response = get_c3po(f"{env_settings.c3po_url}/rule/")

    # approach is all rules for all fields with allowed html tags
    rules = []
    for rule in response.json():
        rule_model = Rule(**rule)

        rules.append(
            {
                "rule_code": rule_model.rule_code,
                "rule_variant": rule_model.rule_variant,
                "description": rule_model.description,
                "severity_level": rule_model.severity_level,
            }
        )

    schemas, _ = collect_structure_data(get_ttl_hash(60))
    schema = schemas["0.4.0"]
    rule_sets: list[RuleSetOut] = []
    for key in schema.keys():
        rule_set = {"code": key, "rules": rules}
        rule_set_model = RuleSetOut(**rule_set)
        if schema[key].allowed_html_tags is None:
            continue
        rule_sets.append(rule_set_model)

    return rule_sets


async def forward_request(body: C3poRequest, user: User) -> C3poResults:
    rule_response = get_c3po(f"{env_settings.c3po_url}/rule/")
    rules = [rule["rule_code"] for rule in rule_response.json()]
    text_raw = strip_html(body.text)
    data: ProcessingRequestOut = {"payload": text_raw, "rule_codes": rules}
    post_response = post_c3po_request(data).json()
    request_id = post_response["processing_request_id"]

    tries = 0
    time.sleep(1)
    max_tries = 60
    results = []
    while tries < max_tries:
        response = get_c3po(f"{env_settings.c3po_url}/processing-request/{request_id}")

        response_model = ProcessingRequest(**response.json())

        results = []
        for task_result in response_model.tasks:
            if task_result.status in ["new", "pending"]:
                continue

            results.append(
                {
                    "rule_code": task_result.rule.rule_code,
                    "description": task_result.rule.description,
                    "feedback_message": task_result.feedback_message,
                    "result": task_result.result,
                }
            )

        if len(results) == len(rules):
            break
        time.sleep(1)
        logger.info(
            f"Collected {len(results)}/{len(rules)} results, trying {max_tries - tries -1} more times..."
        )
        tries += 1

    response = {"rules": results}
    response = C3poResults(**response)
    return response
