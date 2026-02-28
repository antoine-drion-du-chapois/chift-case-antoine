from pydantic import BaseModel
from datetime import datetime


class ContactResponse(BaseModel):
    id: int
    odoo_id: int
    name: str | None
    email: str | None
    write_date: datetime

    class Config:
        from_attributes = True
