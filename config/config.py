from pydantic import computed_field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    MYSQL_USER: str = "user"
    MYSQL_PASSWORD: str = "password"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3307
    MYSQL_DATABASE: str = "main"

    CUSTOMER_SERVICE_BASE_URL: str = "http://localhost:8000"
    INTERNAL_API_KEY: str = "internal-shared-key"
    AUTH_SECRET: str = "dev-seller-auth-secret-change-me"
    AUTH_TOKEN_TTL_MINUTES: int = 120

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6380
    REDIS_TTL: int = 100

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        )
