from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.repositories import invoices_repository
from app.models.invoice import Invoice
from app.core.logger import logger


def list_invoices(db: Session) -> list[Invoice]:
    try:
        invoices = invoices_repository.get_all_invoices(db)
        return invoices
    except SQLAlchemyError:
        logger.exception("Database error while listing invoices")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


def retrieve_invoice(db: Session, invoice_id: int) -> Invoice | None:
    try:
        invoice = invoices_repository.get_invoice_by_id(db, invoice_id)
        return invoice
    except SQLAlchemyError:
        logger.exception(
            "Database error while retrieving invoice id=%s",
            invoice_id
        )
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
