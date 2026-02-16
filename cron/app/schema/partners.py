from pydantic import BaseModel
from datetime import datetime


class OdooPartner(BaseModel):
    odoo_id: int
    name: str | None
    email: str | None
    active: bool
    write_date: datetime | None
