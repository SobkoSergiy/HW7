from libgravatar import Gravatar
from sqlalchemy.orm import Session
from database.models import User
from schemas import UserUpdate, UserCreate


async def get_users(skip: int, limit: int, db: Session) -> list[User]:
    """
    Read all contacts.

    :param db: The database session.
    :type db: Session
    :param current_user: The current user making the request.
    :type current_user: User
    :return: List of contacts.
    :rtype: List[Contact]
    """
    return db.query(User).offset(skip).limit(limit).all()


async def update_user(user_id: int, body: UserUpdate, db: Session) -> User | None:
    """
    Endpoint for update user.

    :param body: The data for creating a new user.
    :type body: UserCreate
    :param body: The data for creating a new user.
    :type body: UserCreate
    :param db: The database session.
    :type db: Session
    :return: Updated user.
    :rtype: User
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:   
        user.username = body.username
        user.roles = body.roles
        user.created = body.created
        user.verified = body.verified
        db.commit()
    return user


async def get_user_by_email(email: str, db: Session) -> User | None:
    """
    Read a user from the database by email.

    :param email: The email address of the user to retrieve.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The user with the specified email, or None if not found.
    :rtype: User | None
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserCreate, db: Session) -> User:
    """
    Creates a new user in the database.

    :param body: The data for the new user.
    :type body: UserModel
    :param db: The database session.
    :type db: Session
    :return: The newly created user.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)

    user = User(email=body.email, password=body.password, username=body.username, avatar=avatar)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Updates the refresh token for a user in the database.

    :param user: The user to update the token for.
    :type user: User
    :param token: The new refresh token, or None.
    :type token: str | None
    :param db: The database session.
    :type db: Session
    """
    user.refresh = token
    db.commit()


async def verify_email(email: str, db: Session) -> None:
    """
    Verify the email address of a user in the database.

    :param email: The email address to confirm.
    :type email: str
    :param db: The database session.
    :type db: Session
    """
    user = await get_user_by_email(email, db)
    if user:
       user.verified = True
    db.commit()


async def remove_user(user_id: int, db: Session) -> User | None:
    """
    Remove user.

    :param user_id: The user's ID.
    :type user_id: int
    :param db: The database session.
    :type db: Session
    :return: Updated user.
    :rtype: User
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user


async def patch_avatar(user: User, avatar: str | None, db: Session) -> None:
    """
    Updates the avatar URL for a user in the database.

    :param email: The email address of the user.
    :type email: str
    :param url: The new avatar URL.
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: The user with the updated avatar URL.
    :rtype: User
    """
    user.avatar = avatar
    db.commit()
    return user 


