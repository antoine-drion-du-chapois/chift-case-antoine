from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.services import invoices_service
from app.schemas.invoice_response import InvoiceResponse
from app.core.logger import logger


router = APIRouter()


@router.get("/", response_model=list[InvoiceResponse])
def get_invoices(
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    logger.info("GET /invoices - Fetching active invoices")
    try:
        invoices = invoices_service.list_invoices(db)
        logger.info("GET /invoices - Returned %s invoices", len(invoices))
        return invoices
    except Exception:
        logger.exception("GET /invoices - Unexpected error")
        raise


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    logger.info("GET /invoices/%s - Fetching invoice", invoice_id)
    try:
        invoice = invoices_service.retrieve_invoice(db, invoice_id)
        if invoice is None:
            logger.warning(
                "GET /invoices/%s - Invoice not found",
                invoice_id
            )
            raise HTTPException(status_code=404, detail="Invoice not found")
        logger.info(
            "GET /invoices/%s - Invoice found",
            invoice_id
        )
        return invoice
    except HTTPException:
        raise
    except Exception:
        logger.exception(
            "GET /invoices/%s - Unexpected error",
            invoice_id
        )
        raise
