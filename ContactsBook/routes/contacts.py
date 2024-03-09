from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter
from database.db import get_db
from database.models import User
from schemas import ContactBase, ContactResponse
from repository import contacts as repository_contacts
from services.auth import auth_service


router = APIRouter(tags=["contacts"])


@router.get("/", response_model=list[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Endpoint for read all contacts.

    :param skip: The database skip contacts.
    :type skip: int
    :param limit: The limit of read contacts.
    :type limit: int
    :param db: The database session.
    :type db: Session
    :param current_user: The current user making the request.
    :type current_user: User
    :return: List of contacts.
    :rtype: List[Contact]
    """
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Endpoint for reading contact with a given ID.

    :param contact_id: The contact's ID.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The current user making the request.
    :type current_user: User
    :return: The newly created contact.
    :rtype: Contact
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact id = {contact_id} (user: '{current_user.email}') not found")
    return contact


@router.get("/find", response_model=list[ContactResponse], dependencies=[Depends(RateLimiter(times=3, seconds=60))])
async def find_contacts(field: str, value: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user),):
    """
    Endpoint for find contacts by specified field.

    :param field: The field to filter the contacts.
    :type field: str
    :param value: The value to filter the contacts.
    :type value: str
    :param db: The database session.
    :type db: Session
    :param current_user: The current user making the request.
    :type current_user: User
    :return: List of contacts.
    :rtype: List[Contact]
    """
    contacts = await repository_contacts.get_contacts_by(field, value, db, current_user)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No contact found")    
    return contacts


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=3, seconds=7))])
async def create_contact(body: ContactBase, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Endpoint for add a new contact.

    :param body: The data for creating a new contact.
    :type body: ContactBase
    :param db: The database session.
    :type db: Session
    :param current_user: The current user making the request.
    :type current_user: User
    :return: The newly created contact.
    :rtype: Contact
    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=3, seconds=7))])
async def update_contact(body: ContactBase, contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Endpoint for update a contact.

    :param body: The updated data for the contact.
    :type body: ContactBase
    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The current user making the request.
    :type current_user: User
    :return: The updated contact.
    :rtype: Contact
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact id = {contact_id} (user: '{current_user.email}') not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=3, seconds=7))])
async def remove_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Endpoint for remove a contact.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The current user making the request.
    :type current_user: User
    :return: The removed contact.
    :rtype: Contact
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact id = {contact_id} (user: '{current_user.email}') not found")
    return contact


@router.get('/birthdays', response_model=list[ContactBase])
async def birthdays(days: int = 7, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Endpoint for find contacts with upcoming birthdays in a given day range.

    :param days: Days range include birthday.
    :type days: int
    :param db: The database session.
    :type db: Session
    :param current_user: The current user making the request.
    :type current_user: User
    :return: List of contacts.
    :rtype: List[Contact]
    """
    contacts = await repository_contacts.soon_birthdays(days, db, current_user)
    return contacts