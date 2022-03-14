from pydantic import BaseSettings


class Settings(BaseSettings):
    log_level: str = "DEBUG"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "CONFIG_"
