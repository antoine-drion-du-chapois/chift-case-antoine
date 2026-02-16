import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.DATABASE_URL: str = os.getenv("DATABASE_URL")
        self.SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key")
        self.ALGORITHM: str = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

        required = [
            self.DATABASE_URL,
            self.SECRET_KEY,
        ]

        if any(v is None for v in required):
            raise ValueError("Missing required environment variables")


settings = Settings()
