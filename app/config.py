from __future__ import annotations

import os
from functools import lru_cache
from urllib.parse import quote_plus, urlencode

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "fastapi-cloud-run-lab"
    app_env: str = "local"

    db_name: str | None = None
    db_user: str | None = None
    db_password: str | None = None
    db_host: str = "127.0.0.1"
    db_port: int = 5432
    instance_connection_name: str | None = None

    database_url_async: str | None = None
    database_url_sync: str | None = None

    @property
    def is_cloud_run(self) -> bool:
        return bool(os.getenv("K_SERVICE"))

    @property
    def use_cloudsql_socket(self) -> bool:
        env = self.app_env.lower()
        return bool(self.instance_connection_name) and (self.is_cloud_run or env in {"prod", "production"})

    def _validate_db_fields(self) -> None:
        required = {
            "DB_NAME": self.db_name,
            "DB_USER": self.db_user,
            "DB_PASSWORD": self.db_password,
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise ValueError(f"Missing DB settings: {', '.join(missing)}")

    @property
    def async_database_url(self) -> str:
        if self.database_url_async:
            return self.database_url_async

        self._validate_db_fields()
        db_user = quote_plus(self.db_user or "")
        db_password = quote_plus(self.db_password or "")

        if self.use_cloudsql_socket:
            socket_path = f"/cloudsql/{self.instance_connection_name}"
            query = urlencode({"host": socket_path})
            return f"postgresql+asyncpg://{db_user}:{db_password}@/{self.db_name}?{query}"

        return f"postgresql+asyncpg://{db_user}:{db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def sync_database_url(self) -> str:
        if self.database_url_sync:
            return self.database_url_sync

        self._validate_db_fields()
        db_user = quote_plus(self.db_user or "")
        db_password = quote_plus(self.db_password or "")

        if self.use_cloudsql_socket:
            socket_path = f"/cloudsql/{self.instance_connection_name}"
            query = urlencode({"host": socket_path})
            return f"postgresql+psycopg://{db_user}:{db_password}@/{self.db_name}?{query}"

        return f"postgresql+psycopg://{db_user}:{db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
