from typing import Iterable

from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.models.contact import Contact


class ContactRepository:

    def bulk_upsert(self, db, rows):
        stmt = insert(Contact).values(rows)

        stmt = stmt.on_conflict_do_update(
            index_elements=["odoo_id"],
            set_={
                "odoo_id": stmt.excluded.odoo_id,
                "name": stmt.excluded.name,
                "email": stmt.excluded.email,
                "active": stmt.excluded.active,
                "write_date": stmt.excluded.write_date,
            },
        )

        db.execute(stmt)
