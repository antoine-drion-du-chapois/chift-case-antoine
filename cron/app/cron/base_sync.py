from abc import ABC, abstractmethod
from datetime import datetime
from time import perf_counter
from sqlalchemy import text


from app.core.database import SessionLocal
from app.core.logger import logger
from app.repositories.sync_state_repository import (
    get_last_sync,
    update_last_sync,
)


class BaseSyncJob(ABC):
    """
        Abstract base class for Odoo synchronization jobs. 
    """

    def __init__(self, job_name, data_repo):
        self.job_name = job_name
        self.data_repo = data_repo

    @abstractmethod
    def fetch(self, last_sync: datetime):
        """
        Initialize Odoo request fields, retrieve updated records
        since last_sync, and parse them into the corresponding DTO objects.
        """
        pass

    def run(self):
        """
        Execute the full synchronization workflow:

        - Acquire PostgreSQL advisory lock (prevents concurrent runs)
        - Retrieve last sync timestamp
        - Fetch updated records from Odoo
        - Bulk upsert into the database
        - Update sync state if needed
        - Commit or rollback transaction
        - Release lock and close DB session
        """
        db = SessionLocal()
        start_time = perf_counter()

        # Deterministic lock per job
        lock_id = abs(hash(self.job_name)) % (2**31)

        logger.info(f"[{self.job_name}] Sync started")

        try:
            # Acquire advisory lock
            lock_acquired = db.execute(
                text("SELECT pg_try_advisory_lock(:id)"),
                {"id": lock_id},
            ).scalar()

            if not lock_acquired:
                logger.info(
                    f"[{self.job_name}] Another instance running. Skipping."
                )
                return

            # Fetch last sync
            last_sync = get_last_sync(db, self.job_name)
            logger.info(f"[{self.job_name}] Last sync = {last_sync}")

            fetch_start = perf_counter()
            records = self.fetch(last_sync)
            fetch_duration = perf_counter() - fetch_start

            logger.info(
                f"[{self.job_name}] Fetched {len(records)} records "
                f"in {fetch_duration:.3f}s"
            )

            if not records:
                logger.info(
                    f"[{self.job_name}] No new records. Sync finished."
                )
                return

            rows = [r.model_dump() for r in records]

            max_write_date = max(
                (r.write_date for r in records if r.write_date),
                default=last_sync
            )

            logger.info(
                f"[{self.job_name}] Max write_date from batch = {max_write_date}"
            )

            upsert_start = perf_counter()
            self.data_repo.bulk_upsert(db, rows)
            upsert_duration = perf_counter() - upsert_start

            logger.info(
                f"[{self.job_name}] Upserted {len(rows)} rows "
                f"in {upsert_duration:.3f}s"
            )

            if max_write_date and max_write_date > last_sync:
                update_last_sync(db, self.job_name, max_write_date)
                logger.info(
                    f"[{self.job_name}] Updated last_sync → {max_write_date}"
                )

            db.commit()

            total_duration = perf_counter() - start_time
            logger.info(
                f"[{self.job_name}] Sync committed successfully "
                f"in {total_duration:.3f}s"
            )

        except Exception:
            logger.exception(
                f"[{self.job_name}] Sync failed. Rolling back."
            )
            db.rollback()
            raise

        finally:
            # Always release advisory lock
            try:
                db.execute(
                    text("SELECT pg_advisory_unlock(:id)"),
                    {"id": lock_id},
                )
            except Exception:
                pass

            db.close()
            logger.info(f"[{self.job_name}] DB session closed")
