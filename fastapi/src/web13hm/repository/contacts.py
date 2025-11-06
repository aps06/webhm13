from typing import List

from fastapi import HTTPException, status

from sqlalchemy import or_
from sqlalchemy.orm import Session

from datetime import date, timedelta

from src.web13hm.database.models import Contacts, User
from src.web13hm.shemas import ContactModel, ResponseContactModel


async def get_Contacts(
    skip: int, limit: int, user: User, db: Session
) -> List[ResponseContactModel]:
    contacts = (
        db.query(Contacts)
        .filter(Contacts.user_id == user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return contacts


async def get_Contacts_by(
    Contacts_data: int | str, user: User, db: Session
) -> List[ResponseContactModel]:
    conditions = [
        Contacts.name == Contacts_data,
        Contacts.last_name == Contacts_data,
        Contacts.email == Contacts_data,
    ]

    if Contacts_data.isdigit():
        conditions.append(Contacts.id == int(Contacts_data))

    contacts = (
        db.query(Contacts).filter(or_(*conditions), Contacts.user_id == user.id).all()
    )

    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


async def birthday_by_7_day(
    skip: int,
    limit: int,
    db: Session,
    current_user: User,
) -> List[ResponseContactModel]:
    date_by_7_day = date.today() + timedelta(days=7)
    print("today-{date.today()}, 7 {date_by_7_day}")
    contacts = (
        db.query(Contacts)
        .filter(Contacts.birthday <= date_by_7_day, Contacts.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return contacts


async def create_contact(contact: ContactModel, db: Session, current_user: User):
    new_contact = Contacts(
        name=contact.name,
        last_name=contact.last_name,
        email=contact.email,
        number=contact.number,
        birthday=contact.birthday,
        user_id=current_user.id,
        extra_data=contact.extra_data,
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


async def delete_contact(
    contact_id: int,
    db: Session,
    current_user: User,
):
    contact_db = (
        db.query(Contacts)
        .filter(Contacts.id == contact_id, Contacts.user_id == current_user.id)
        .first()
    )
    if not contact_db:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact_db)
    db.commit()
    return {"ok": True}


async def update_contact(
    contact_id: int, contact: ContactModel, db: Session, current_user: User
):
    contacts_db = (
        db.query(Contacts)
        .filter(Contacts.id == contact_id, Contacts.user_id == current_user.id)
        .first()
    )
    if not contacts_db:
        raise HTTPException(status_code=404, detail="Contact not found")
    contacts_db.name = contact.name
    contacts_db.last_name = contact.last_name
    contacts_db.email = contact.email
    contacts_db.number = contact.number
    contacts_db.birthday = contact.birthday
    contacts_db.extra_data = contact.extra_data
    db.commit()
    db.refresh(contacts_db)
    return contacts_db
