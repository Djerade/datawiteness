from functools import cached_property

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=("../.env", ".env"), extra="ignore")

    api_env: str = "dev"
    api_cors_origins: str = "http://localhost:5173"
    database_url: str = "postgresql+psycopg://datawitness:datawitness@localhost:5432/datawitness"
    storage_dir: str = "../data/raw"

    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    llm_provider: str = "anthropic"
    llm_model: str = "claude-sonnet-5-5"
    anthropic_api_key: str = ""

    match_similarity_threshold: float = 0.78
    divergence_relative_tolerance: float = 0.02

    @cached_property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.api_cors_origins.split(",") if o.strip()]


settings = Settings()
