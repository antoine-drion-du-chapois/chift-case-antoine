from sqlalchemy.orm import Session
from app.models.contact import Contact
from sqlalchemy import and_


def get_contact_by_id(db: Session, contact_id: int) -> Contact | None:
    return (
        db.query(Contact)
        .filter(
            and_(
                Contact.id == contact_id,
                Contact.active.is_(True)
            )
        )
        .first()
    )


def get_all_contacts(db: Session) -> list[Contact]:
    return (
        db.query(Contact)
        .filter(Contact.active.is_(True))
        .all()
    )
