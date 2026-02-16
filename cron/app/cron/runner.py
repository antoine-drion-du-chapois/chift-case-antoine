from app.cron.contacts_sync import ContactsSyncJob
from app.cron.invoices_sync import InvoicesSyncJob
from app.core.logger import logger


def run_all_jobs():
    """
    Execute the full synchronization cycle.

    This function instantiates all registered sync jobs
    (e.g. contacts, invoices) and runs them sequentially.
    Each job is responsible for:
        - Fetching updated data from Odoo
        - Persisting data into the database
        - Handling its own transaction lifecycle

    """
    logger.info("Starting full sync cycle")

    jobs = [
        ContactsSyncJob(),
        InvoicesSyncJob(),
    ]

    for job in jobs:
        job.run()

    logger.info("All jobs completed")
