from typing import Iterable
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.core.logger import logger
from app.models.invoice import Invoice
from app.repositories.abstract_repository import AbstractRepository


class InvoiceRepository(AbstractRepository):

    def bulk_upsert(self, db, rows):
        if not rows:
            return

        stmt = insert(Invoice).values(rows)
        # Insertion en cas de non existance et update en cas d'existance
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

        result = db.execute(stmt)

        if result.rowcount != len(rows):
            logger.warning(
                f"Expected {len(rows)} rows affected, got {result.rowcount}"
            )
