# Native imports

# Third party imports
from fastapi import FastAPI

# Custom imports
from api_bedofih_2017.api.routes import router as v1_router
from api_bedofih_2017.config import settings


app = FastAPI(
    title=settings.project_name,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.include_router(v1_router, prefix="/api")