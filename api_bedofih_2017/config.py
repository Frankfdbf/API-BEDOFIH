# Native imports
import logging

# Third party imports
from pydantic_settings import BaseSettings

# Custom imports


logging.basicConfig(level=logging.INFO)

class Settings(BaseSettings):
    """App settings."""

    project_name: str = "api_bedofih_2017"
    debug: bool = False
    environment: str = "local"

    # Database
    DATABASE_URL: str =  ""


settings = Settings()