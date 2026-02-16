from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.services import contacts_service
from app.schemas.contact_response import ContactResponse
from app.core.logger import logger


router = APIRouter()


@router.get("/", response_model=list[ContactResponse])
def get_contacts(
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    logger.info("GET /contacts - Fetching active contacts")
    try:
        contacts = contacts_service.list_contacts(db)
        logger.info("GET /contacts - Returned %s contacts", len(contacts))
        return contacts
    except Exception as e:
        logger.exception("GET /contacts - Unexpected error")
        raise


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    logger.info("GET /contacts/%s - Fetching contact", contact_id)
    try:
        contact = contacts_service.retrieve_contact(db, contact_id)
        if contact is None:
            logger.warning(
                "GET /contacts/%s - Contact not found",
                contact_id
            )
            raise HTTPException(status_code=404, detail="Contact not found")
        logger.info(
            "GET /contacts/%s - Contact found",
            contact_id
        )
        return contact
    except HTTPException:
        raise
    except Exception:
        logger.exception(
            "GET /contacts/%s - Unexpected error",
            contact_id
        )
        raise
