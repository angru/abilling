import os

from pydantic import BaseSettings


class Config(BaseSettings):
    DB_PG_NAME: str = 'postgres'
    DB_PG_SCHEMA: str = 'public'
    DB_PG_USERNAME: str
    DB_PG_PASSWORD: str
    DB_PG_HOST: str
    DB_PG_PORT: int = 5432

    @property
    def DB_PG_URL(self):
        return 'postgresql://{user}:{password}@{host}:{port}/{db_name}'.format(
            user=self.DB_PG_USERNAME,
            password=self.DB_PG_PASSWORD,
            host=self.DB_PG_HOST,
            port=self.DB_PG_PORT,
            db_name=self.DB_PG_NAME,
        )


config = Config(_env_file=os.environ.get('ENV_FILE'))