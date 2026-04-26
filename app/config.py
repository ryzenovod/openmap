from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Medical Geo Analytics Backend"
    app_env: str = "dev"
    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/openmap"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="OPENMAP_")


settings = Settings()
