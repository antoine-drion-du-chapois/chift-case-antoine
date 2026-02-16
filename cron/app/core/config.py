import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.DATABASE_URL: str = os.getenv("DATABASE_URL")
        self.ODOO_URL: str = os.getenv("ODOO_URL")
        self.ODOO_DB: str = os.getenv("ODOO_DB")
        self.ODOO_USERNAME: str = os.getenv("ODOO_USERNAME")
        self.ODOO_PASSWORD: str = os.getenv("ODOO_PASSWORD")
        self.SYNC_INTERVAL_MINUTE: str = os.getenv("SYNC_INTERVAL_MINUTES")

        required = [
            self.DATABASE_URL,
            self.ODOO_URL,
            self.ODOO_DB,
            self.ODOO_USERNAME,
            self.ODOO_PASSWORD,
        ]

        if any(v is None for v in required):
            raise ValueError("Missing required environment variables")


settings = Settings()
