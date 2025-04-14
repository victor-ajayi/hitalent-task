from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_NAME: str

    DEBUG: bool = False

    @computed_field
    @property
    def get_database_url(self) -> str:
        if self.DEBUG == False:
            return self.postgres_url
        else:
            return "sqlite:///db.sqlite3"

    @computed_field
    @property
    def postgres_url(self) -> str:
        return str(
            MultiHostUrl.build(
                scheme="postgresql+psycopg2",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_NAME,
            )
        )

    @computed_field
    @property
    def test_postgres_url(self) -> str:
        return str(
            MultiHostUrl.build(
                scheme="postgresql+psycopg2",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path="test",
            )
        )


settings = Settings()
