import os
from dotenv import load_dotenv


load_dotenv()

class RunConfig:
    host: str = "0.0.0.0"
    port: int = 8000


class ApiPrefix:
    authors: str = "/authors"
    books: str = "/books"
    borrows: str = "/borrows"


class DatabaseConfig:
    user: str = os.getenv('DB_USER')
    password: str = os.getenv('DB_PASSWORD')
    db: str = os.getenv('DB_NAME')
    host: str = os.getenv('DB_HOST')
    port: str = os.getenv('DB_PORT')
    echo: bool = True

    @property
    def url(self):
        return "postgresql+asyncpg://" + self.user + ":" + self.password + "@" + \
               self.host + ":" + self.port + "/" + self.db


class Settings:
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig = DatabaseConfig()


settings = Settings()