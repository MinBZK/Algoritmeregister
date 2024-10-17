import os
import requests
import time
from sqlalchemy import func
from app.database.database import SessionLocal
from sqlalchemy.orm import Session
from app.repositories.algoritme_version import AlgoritmeVersionRepository
from app.schemas.misc import Language
from app.models.dashboard_models.broken_links import BrokenLinks
from etl.logger import get_logger

logger = get_logger()

C3PO_URL = os.getenv("C3PO_URL")
if C3PO_URL:
    BASE_URL = C3PO_URL + "/processing-request/"
else:
    raise EnvironmentError("C3PO_URL environment variable is not set.")


def get_batch_number(db: Session) -> int:
    return db.query(func.coalesce(func.max(BrokenLinks.batch) + 1, 1)).scalar()


def check_broken_link(db: Session, lang: Language, current_batch: int):
    algoritme_version_repo = AlgoritmeVersionRepository(db)
    latest_algos = algoritme_version_repo.get_published_by_lang(lang)
    for algo in latest_algos:
        algo_dict = algo.dict()
        payload_values_str = " , ".join(map(str, algo_dict.values()))

        message = {
            "org_code": "ictu-devops",
            "project_code": "algreg",
            "payload": payload_values_str,
            "rule_code": "BROKEN_LINKS",
        }
        for _ in range(5):
            try:
                result = requests.post(url="%s" % (BASE_URL), json=message)
                break
            except requests.exceptions.ChunkedEncodingError:
                time.sleep(60)
            except requests.exceptions.ConnectionError:
                logger.error("Connection with Expert Service not found")
                return

        if result.status_code != 200:
            logger.error(f"Request failed with status code {result.status_code}")
            continue

        response_json = result.json()

        if not response_json:
            logger.error("No data received")
            continue

        if response_json.get("passed"):
            continue

        broken_links = response_json.get("result")
        if not broken_links:
            broken_links = "No broken links found"
        broken_links_results = BrokenLinks(
            lars=algo.lars,
            name=algo.name,
            organisation=algo.organization,
            batch=current_batch,
            broken_links=broken_links,
            language=lang,
        )
        db.add(broken_links_results)
    db.commit()


def main():
    db = SessionLocal()
    batch = get_batch_number(db)
    for lang in Language:
        check_broken_link(db, lang, batch)
    db.close()


if __name__ == "__main__":
    main()
