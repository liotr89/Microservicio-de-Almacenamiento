import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Evidence Storage Service"
    app_version: str = "1.0.0"

    # Azure Storage / Azurite configuration
    azurite_account_name: str = "devstoreaccount"
    azurite_account_key: str = "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBekSoGMHgHb=="
    azurite_blob_endpoint: str = "http://azurite:10000/devstoreaccount"
    azurite_container_name: str = "evidences"

    # API configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8080

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
