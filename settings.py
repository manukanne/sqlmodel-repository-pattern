from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings class, holds all app settings.
    """
    database_connection_str: str = Field(..., env="DATABASE_CONNECTION_STR")

    class Config:
        env_prefix = ""
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
