import os
import json
from pathlib import Path
from app import schemas
from functools import lru_cache


def get_supplier_names(standard_version: str) -> list[str]:
    filenames = os.listdir(f"app/data/templates/{standard_version}")
    return [filename[:-5] for filename in filenames]


@lru_cache(maxsize=3)
def get_supplier_templates(
    supplier: str, standard_version: str
) -> list[schemas.AlgoritmeVersionTemplate]:
    file_path = Path(f"app/data/templates/{standard_version}/{supplier}.json")
    with open(file_path, "r") as filehandler:
        json_obj = json.load(filehandler)
        return [schemas.AlgoritmeVersionTemplate(**template) for template in json_obj]


@lru_cache(maxsize=1)
def get_template_summary(standard_version: str) -> list[schemas.StandardSupplier]:
    suppliers = get_supplier_names(standard_version)

    suppliers_summary: list[schemas.StandardSupplier] = []
    for supplier in suppliers:
        templates = get_supplier_templates(supplier, standard_version)

        templates_summary = []
        for template in templates:
            templates_summary.append(
                schemas.TemplateSummary(name=template.name, id=template.id)
            )

        supplier_summary = schemas.StandardSupplier(
            name=supplier, algorithm_descriptions=templates_summary
        )
        suppliers_summary.append(supplier_summary)
    return suppliers_summary


def get_template_by_id(
    standard_version: str, id: str
) -> schemas.AlgoritmeVersionTemplate | None:
    suppliers = get_supplier_names(standard_version)

    templates: list[schemas.AlgoritmeVersionTemplate] = []
    for supplier in suppliers:
        templates.extend(get_supplier_templates(supplier, standard_version))

    for template in templates:
        print(template)
        if id == template.id:
            return template
