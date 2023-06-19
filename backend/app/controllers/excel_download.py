import datetime
from io import BytesIO
import pandas as pd
from fastapi.responses import StreamingResponse
from app import schemas
from app.controllers.algoritme_version.util import get_latest_versions_algo

excel_schema = schemas.get_algorithm_export_schema(truncated=True)


def prepare_download(db, org_name: str):
    """
    Prepare algorithm data for download.
    If org_name is None, return all data else filter on org_name
    """
    algorithms = get_latest_versions_algo(org_name, db)
    # Use schema to filter output of query
    data = [excel_schema.from_orm(row).dict() for row in algorithms]
    df = pd.DataFrame(data)
    df = df.replace(r"\n", "", regex=True)
    return df


def generate_excel_download(db, org_name):
    df = prepare_download(db, org_name).T
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    filename = f"overzicht_algoritmen_{timestamp}.xlsx"
    file_object = BytesIO()
    df.to_excel(file_object, index=True, header=False)
    file_object.seek(0)
    headers = {"Content-Disposition": f"attachment; {filename}"}
    media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return StreamingResponse(file_object, headers=headers, media_type=media_type)
