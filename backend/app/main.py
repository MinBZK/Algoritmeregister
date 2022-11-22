from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from app.routers import default

app = FastAPI(docs_url="/api-docs", title="Application API")

router = APIRouter()
app.include_router(default.router, prefix="/api")


app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
