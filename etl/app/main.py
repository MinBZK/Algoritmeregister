from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.services import Extractor, Transformer, Loader

app = FastAPI(
    docs_url="/api-docs",
    title="ETL Algoritmeregister",
    swagger_ui_parameters={
        "displayRequestDuration": True,
        "defaultModelsExpandDepth": -1,
    },
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def read_index():
    return FileResponse("app/static/index.html")


@app.get("/load", response_model=dict[str, str])
async def load() -> dict[str, str]:
    json = Extractor().get_json()

    transformer = Transformer(json)
    df_organisation = transformer.json_to_df(table_name="organisation")
    df_organisation_details = transformer.json_to_df(table_name="organisation_details")
    df_algoritme = transformer.json_to_df(table_name="algoritme")
    df_algoritme_version = transformer.json_to_df(table_name="algoritme_version")

    Loader().update_database(
        df_organisation, df_organisation_details, df_algoritme, df_algoritme_version
    )

    return {"message": "Update gelukt!"}
