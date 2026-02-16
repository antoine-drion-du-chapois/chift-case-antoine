from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.invoice import Invoice


def get_invoice_by_id(db: Session, invoice_id: int) -> Invoice | None:
    return (
        db.query(Invoice)
        .filter(
            and_(
                Invoice.id == invoice_id,
            )
        )
        .first()
    )


def get_all_invoices(db: Session) -> list[Invoice]:
    return (
        db.query(Invoice)
        .all()
    )
