from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.repositories import contacts_repository
from app.models.contact import Contact
from app.core.logger import logger


def list_contacts(db: Session) -> list[Contact]:
    try:
        contacts = contacts_repository.get_all_contacts(db)
        return contacts
    except SQLAlchemyError as e:
        logger.exception("Database error while listing contacts")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


def retrieve_contact(db: Session, contact_id: int) -> Contact | None:
    try:
        contact = contacts_repository.get_contact_by_id(db, contact_id)
        return contact
    except SQLAlchemyError:
        logger.exception(
            "Database error while retrieving contact id=%s",
            contact_id
        )
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
