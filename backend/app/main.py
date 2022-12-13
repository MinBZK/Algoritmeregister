from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from app.routers import default, aggregations
from app.etl.load import load
from app.util.logger import get_logger


logger = get_logger(__name__)

data_loaded = load()
if data_loaded:
    logger.info("Algoritmes loaded")
else:
    logger.info("Data not loaded")

app = FastAPI(docs_url="/api-docs", title="Application API")

router = APIRouter()
app.include_router(default.router, prefix="/api", tags=["default"])

router = APIRouter()
app.include_router(aggregations.router, prefix="/api", tags=["aggregations"])

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)
