from apscheduler.schedulers.blocking import BlockingScheduler
from app.cron.runner import run_all_jobs
from app.core.logger import logger
import os
from app.core.config import settings


def start_scheduler():
    scheduler = BlockingScheduler()

    interval = int(settings.SYNC_INTERVAL_MINUTE, 5)

    scheduler.add_job(
        run_all_jobs,
        "interval",
        minutes=interval,
        id="odoo_sync",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    logger.info(f"Scheduler started (interval={interval} min)")
    scheduler.start()


if __name__ == "__main__":
    start_scheduler()
