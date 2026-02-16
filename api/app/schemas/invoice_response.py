from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal


class InvoiceResponse(BaseModel):
    odoo_id: int
    name: str | None
    amount_total: Decimal
    invoice_date: date | None
    write_date: datetime

    class Config:
        from_attributes = True
