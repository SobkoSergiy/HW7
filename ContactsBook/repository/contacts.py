from datetime import date
from sqlalchemy import and_
from sqlalchemy.orm import Session
from database.models import Contact, User
from schemas import ContactBase


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> list[Contact]:
    """
    Read all contacts for user from the database.

    :param db: The database session.
    :type db: Session
    :param user: The user whose contacts are being retrieved.
    :type user: User
    :return: A list of contacts belonging to the user.
    :rtype: List[Contact]
    """
    return (db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all())


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    Read a specific contact by its ID for user from the database.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :param user: The user whose contact is being retrieved.
    :type user: User
    :return: The contact with the specified ID belonging to the user.
    :rtype: Contact
    """
    return (db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first())
    # return db.query(Contact).filter(Contact.id == Contact_id, Contact.user_id == user.id).first()


async def create_contact(body: ContactBase, user: User, db: Session) -> Contact:
    """
    Creates a new contact for user in the database.

    :param body: The data for the new contact.
    :type body: ContactBase
    :param db: The database session.
    :type db: Session
    :param user: The user for whom the contact is being created.
    :type user: User
    :return: The newly created contact.
    :rtype: Contact
    """
    contact = Contact()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.phone = body.phone
        contact.inform = body.inform
        contact.birthday = body.birthday
        contact.email = body.email
        contact.user_id = user.id
        db.add(contact)
        db.commit()
        db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactBase, user: User, db: Session) -> Contact | None:
    """
    Updates an existing contact in the database.

    :param contact: The contact to update.
    :type contact: Contact
    :param body: The updated data for the contact.
    :type body: ContactBase
    :param db: The database session.
    :type db: Session
    :return: The updated contact.
    :rtype: Contact
    """
    contact = (db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first())
    if contact:  
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.phone = body.phone
        contact.inform = body.inform
        contact.birthday = body.birthday
        contact.email = body.email
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    Removes an existing contact from the database.

    :param contact: The contact to remove.
    :type contact: Contact
    :param db: The database session.
    :type db: Session
    """
    contact = (db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first())
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def soon_birthdays(days: int, db: Session, user: User) -> list[Contact]:
    """
    Find contacts with upcoming birthdays in a given day range.

    :param days: Days range include birthday.
    :type days: int
    :param db: The database session.
    :type db: Session
    :param user: The user whose contacts are find.
    :type user: User
    :return: A list of user's contacts with upcoming birthdays.
    :rtype: List[Contact]
    """
    if days > 365:
        days = 365
    res = []
    today = date.today()   # today = date(1986, 12, 25)
    for i in db.query(Contact).filter(Contact.user_id == user.id).all():
        bd = date(today.year, i.birthday.month, i.birthday.day)
        if bd < today:
            bd = bd.replace(year=today.year + 1)
        day_to = (bd - today).days   
        if (day_to <= days):
            res.append(i)
    return res


async def get_contact_by_id(contact_id: str, db: Session, user: User) -> list[Contact]:
    """
    Find a contact by its ID for user from the database.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: str
    :param db: The database session.
    :type db: Session
    :param user: The user whose contact is being retrieved.
    :type user: User
    :return: A list containing the user's contact with the specified ID.
    :rtype: List[Contact]
    """
    contacts = []
    try:
        contact_id = int(contact_id)
    except:
        return contacts
    return (db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).all())


async def get_contacts_by_first_name(first_name: str, db: Session, user: User) -> list[Contact]:
    """
    Find contacts by their first name for user from the database.

    :param first_name: The first name of the contacts to retrieve.
    :type first_name: str
    :param db: The database session.
    :type db: Session
    :param user: The user whose contacts are being retrieved.
    :type user: User
    :return: A list of user's contacts with the specified first name.
    :rtype: List[Contact]
    """
    return (db.query(Contact).filter(Contact.first_name == first_name, Contact.user_id == user.id).all())


async def get_contacts_by_last_name(last_name: str, db: Session, user: User) -> list[Contact]:
    """
    Find contacts by their last name for user from the database.

    :param last_name: The last name of the contacts to retrieve.
    :type last_name: str
    :param db: The database session.
    :type db: Session
    :param user: The user whose contacts are being retrieved.
    :type user: User
    :return: A list of user's contacts with the specified last name.
    :rtype: List[Contact]
    """
    return (db.query(Contact).filter(Contact.last_name == last_name, Contact.user_id == user.id).all())


async def get_contact_by_email(contact_email: str, db: Session, user: User) -> list[Contact]:
    """
    Find a contact by its email address for user from the database.

    :param contact_email: The email address of the contact to retrieve.
    :type contact_email: str
    :param db: The database session.
    :type db: Session
    :param user: The user whose contact is being retrieved.
    :type user: User
    :return: A list containing the user's contact with the specified email address.
    :rtype: List[Contact]
    """
    return (db.query(Contact).filter(Contact.email == contact_email, Contact.user_id == user.id).all())


async def get_contacts_by(field: str, value: str, db: Session, user: User) -> list[Contact]:
    """
    Find contacts by a specified field and value for user from the database.

    :param field: The field to filter the contacts by ("id", "first_name", "last_name", "email").
    :type field: str
    :param value: The value to filter the contacts by.
    :type value: str
    :param db: The database session.
    :type db: Session
    :param user: The user whose contacts are being retrieved.
    :type user: User
    :return: A list of user's contacts filtered by the specified field and value.
    :rtype: List[Contact]
    """

    fields = {
        "id": get_contact_by_id,
        "first_name": get_contacts_by_first_name,
        "last_name": get_contacts_by_last_name,
        "email": get_contact_by_email,
    }

    # contacts = await fields[field](value, db, user) if field in fields.keys() else []
    contacts = []
    if field in fields.keys():
        contacts = await fields[field](value, db, user)

    return contacts


