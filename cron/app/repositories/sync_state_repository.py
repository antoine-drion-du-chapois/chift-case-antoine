from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session


def get_last_sync(db: Session, job_name: str) -> datetime | None:
    """
    Return the last_sync timestamp for a given job.
    """
    result = db.execute(
        text("SELECT last_sync FROM sync_state WHERE job_name = :job"),
        {"job": job_name},
    ).fetchone()

    return result[0] if result else None


def update_last_sync(db: Session, job_name: str, ts: datetime) -> None:
    """
    Update the last_sync timestamp for a given job.
    """
    db.execute(
        text("""
            UPDATE sync_state
            SET last_sync = :ts
            WHERE job_name = :job
        """),
        {"ts": ts, "job": job_name},
    )
