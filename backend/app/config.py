import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    chroma_persist_directory: str = os.getenv("CHROMA_DIR", "chroma_db")
    model_name: str = os.getenv("MODEL_NAME", "gpt-4o-mini")  # adjust as needed


class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"


settings = Settings()
