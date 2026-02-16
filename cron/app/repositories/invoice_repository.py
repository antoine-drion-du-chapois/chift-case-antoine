from typing import Iterable

from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.models.invoice import Invoice
from app.repositories.abstract_repository import AbstractRepository


class InvoiceRepository(AbstractRepository):

    def bulk_upsert(self, db, rows):
        stmt = insert(Invoice).values(rows)

        stmt = stmt.on_conflict_do_update(
            index_elements=["odoo_id"],
            set_={
                "odoo_id": stmt.excluded.odoo_id,
                "name": stmt.excluded.name,
                "amount_total": stmt.excluded.amount_total,
                "invoice_date": stmt.excluded.invoice_date,
                "write_date": stmt.excluded.write_date,
            },
        )

        db.execute(stmt)
