from typing import Iterable
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime
from app.models.contact import Contact
from app.core.logger import logger


class ContactRepository:

    def bulk_upsert(self, db, rows):
        if not rows:
            return

        stmt = insert(Contact).values(rows)

        stmt = stmt.on_conflict_do_update(
            index_elements=["odoo_id"],
            set_={
                "name": stmt.excluded.name,
                "email": stmt.excluded.email,
                "active": stmt.excluded.active,
                "write_date": stmt.excluded.write_date,
            },
        )

        db.execute(stmt)
