from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_host: str = "127.0.0.1"
    postgres_port: int = 5432
    postgres_database: str = "books_db"
    postgres_driver: str = "psycopg"

    model_config = SettingsConfigDict(env_prefix='books_api_')

    @property
    def sqlalchemy_url(self):
        return (f"postgresql+{self.postgres_driver}://{self.postgres_user}:{self.postgres_password}@"
                f"{self.postgres_host}:{self.postgres_port}/{self.postgres_database}")

settings = Settings()