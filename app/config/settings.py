import logging
import os
from datetime import timedelta
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv(dotenv_path="./.env")


def setup_logging():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


class LLMSettings(BaseModel):
    temperature: float = 0.0
    max_tokens: Optional[int] = None
    max_retries: int = 3


class OpenAISettings(LLMSettings):
    api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    default_model: str = Field(default="gpt-4o")
    embedding_model: str = Field(default="text-embedding-3-small")


class DatabaseSettings(BaseModel):
    service_url: str = Field(default_factory=lambda: os.getenv("TIMESCALE_SERVICE_URL"))


class VectorStoreSettings(BaseModel):
    table_name: str = "magazines"
    embedding_dimensions: int = 1536
    time_partition_interval: timedelta = timedelta(days=7)

class Settings(BaseModel):
    openai: OpenAISettings = Field(default_factory=OpenAISettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    vector_store: VectorStoreSettings = Field(default_factory=VectorStoreSettings)


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    setup_logging()
    return settings
