from app.cron.base_sync import BaseSyncJob
from app.models.invoice import Invoice
from app.repositories.invoice_repository import InvoiceRepository
from app.odoo.client import _fetch_generic
from app.schema.invoice import OdooInvoice


class InvoicesSyncJob(BaseSyncJob):

    def __init__(self):
        super().__init__(
            job_name="invoices_sync",
            data_repo=InvoiceRepository()
        )

    def fetch(self, last_sync):
        fields = [
            "id",
            "name",
            "amount_total",
            "invoice_date",
            "write_date",
        ]

        raw_records = _fetch_generic(
            model="account.move",
            last_sync=last_sync,
            fields=fields,
        )

        return [
            OdooInvoice(
                odoo_id=r["id"],
                name=r.get("name") or None,
                amount_total=r["amount_total"],
                invoice_date=r.get("invoice_date") or None,
                write_date=r.get("write_date") or None,
            )
            for r in raw_records
        ]
