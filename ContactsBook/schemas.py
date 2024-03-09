from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel): 
    """
    Schema representing the structure of a user model.

    Attributes:
        email (str): The email address of the user.
        password (str): The password of the user.
        username (str | None): The name of the user.
        roles (str | None): The role of the user.
    """
    email: EmailStr
    password: str
    username: str | None


class UserUpdate(BaseModel): 
    """
    Schema representing the base structure of a user model.

    Attributes:
        username (str | None): The name of the user.
        roles (str | None): The role of the user.
        created (datetime): The created date of the user.
        verified (bool): The verification of the user.
    """
    username: str
    roles: str
    created: datetime
    verified: bool


# class UserLogin(BaseModel):
# # class UserIn(BaseModel):
#     """
#     Schema representing the structure of a user model.

#     Attributes:
#         email (str): The email address of the user.
#         password (str): The password of the user.
#     """
#     email:str
#     password: str


class UserDB(BaseModel):
    """
    Schema representing the structure of a user from the database.

    Attributes:
        id (int): The ID of the user.
        email (str): The email address of the user.
        username (str | None): The name of the user.
        roles (str | None): The role of the user.
        avatar (str | None): The avatar URL of the user, or None if not available.
        created (datetime): The created date of the user.
        verified (bool): The verification of the user.
    """
    id: int
    email: str      # = Field(pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    username: str | None
    roles: str | None
    avatar: str | None
    created: datetime
    verified: bool
    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """
    Schema representing the response structure for a user.

    Attributes:
        user (UserDB): Base structure of a user.
        detail (str): Information message indicating user creation success.
    """
    user: UserDB
    detail: str = "User successfully created"


class UserUpdateAvatar(BaseModel):
    """
    Schema representing the structure of a user avatar.

    Attributes:
        avatar (str): The avatar URL of the user.
    """
    avatar: str


class TokenModel(BaseModel):
    """
    Schema representing the structure of a token.

    Attributes:
        access_token (str): The access token.
        refresh_token (str): The refresh token.
        token_type (str): The token type (default is "bearer").
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ContactBase(BaseModel):
    """
    Schema representing the base structure of a contact.

    Attributes:
        first_name (str): The first name of the contact.
        last_name (str): The last name of the contact.
        phone (str): The phone number of the contact.
        birthday (datetime): The birth date of the contact, must be in the past.
        inform (str): Additional information about the contact.
        email (str): The email address of the contact.
    """
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=30)
    phone: str = Field(max_length=13)   # Field(pattern=r'^\d{13}$'))
    birthday: datetime                  # Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    inform: str = Field(max_length=150)
    email: str   


class ContactResponse(ContactBase):
    """
    Schema representing the response structure for a contact.

    Inherits:
        ContactBase: Base structure of a contact.

    Attributes:
        id (int): The ID of the contact.
        user_id (int): The ID of the user.
    """
    id: int
    user_id: int        
    class Config:
        from_attributes = True


class RequestEmail(BaseModel):
    """
    Schema representing the structure of a request email.

    Attributes:
        email (str): The email address.
    """
    email: EmailStr
