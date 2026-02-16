from datetime import datetime, date
from pydantic import BaseModel
from decimal import Decimal


class OdooInvoice(BaseModel):
    odoo_id: int
    name: str | None
    amount_total: Decimal
    invoice_date: date | None
    write_date: datetime
