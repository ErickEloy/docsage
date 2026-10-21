from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # API Settings
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True

    # LLM & Embedding Settings
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"

    # Vector Store Settings
    chroma_persist_directory: str = "./chroma_data"
    chunk_size: int = 1000
    chunk_overlap: int = 200


settings = Settings()