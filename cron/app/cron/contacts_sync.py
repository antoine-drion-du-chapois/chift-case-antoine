from app.cron.base_sync import BaseSyncJob
from app.models.contact import Contact
from app.repositories.contact_repository import ContactRepository
from app.odoo.client import _fetch_generic
from app.schema.partners import OdooPartner


class ContactsSyncJob(BaseSyncJob):

    def __init__(self):
        super().__init__(
            job_name="contacts_sync",
            data_repo=ContactRepository(),
        )

    def fetch(self, last_sync):
        fields = [
            "id",
            "name",
            "email",
            "active",
            "write_date",
        ]

        raw_records = _fetch_generic(
            model="res.partner",
            last_sync=last_sync,
            fields=fields,
        )

        return [
            OdooPartner(
                odoo_id=r["id"],
                name=r.get("name"),
                email=r.get("email"),
                active=r.get("active", True),
                write_date=r.get("write_date"),
            )
            for r in raw_records
        ]
