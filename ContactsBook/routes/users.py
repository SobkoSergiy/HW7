from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from fastapi.security import HTTPBearer
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from database.db import get_db
from schemas import UserUpdate, UserDB
from repository import users as repository_users
from services.auth import auth_service
from services.config import settings
from database.models import User
import cloudinary
import cloudinary.uploader


router = APIRouter(tags=["users"])
security = HTTPBearer()


@router.get("/", response_model=list[UserDB])
async def read_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """
    Endpoint for read all users.

    :param skip: The database skip users.
    :type skip: int
    :param limit: The limit of read users.
    :type limit: int
    :param db: The database session.
    :type db: Session
    :return: List of User.
    :rtype: List[User]
    """
    users = await repository_users.get_users(skip, limit, db)
    return users


@router.get("/me", response_model=UserDB)
async def read_users_me(current_user: Annotated[User, Depends(auth_service.get_current_user)]):
    """
    Endpoint for read the current user's information.

    :param current_user: The current user making the request.
    :type current_user: User
    :return: The current user's information.
    :rtype: User
    """
    return current_user


@router.get("/me/items")
async def read_items(current_user: Annotated[User, Depends(auth_service.get_current_user)]):
    """
    Endpoint for read the current user's information.

    :param current_user: The current user making the request.
    :type current_user: User
    :return: The current user's information.
    :rtype: User
    """
    return [{"id": current_user.id, "email": current_user.email}]


@router.get("/config")
async def config():
    """
    Endpoint for read the config information.

    :return: The config information.
    :rtype: dict
    """
    return {"app_name": settings.project_name, "admin_email": settings.admin_email}


@router.put("/{user_id}", response_model=UserDB)
async def update_user(user_id: int, body: UserUpdate, db: Session = Depends(get_db)):
    """
    Endpoint for update user.

    :param user_id: The user's ID.
    :type user_id: int
    :param body: The data for updating a new user.
    :type body: UserUpdate
    :param db: The database session.
    :type db: Session
    :return: Updated user.
    :rtype: User
    """
    user = await repository_users.update_user(user_id, body, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User id = {user_id} not found")
    return user


@router.delete("/{user_id}", response_model=UserDB)
async def remove_user(user_id: int, db: Session = Depends(get_db)):
    """
    Endpoint for remove user.

    :param user_id: The user's ID.
    :type user_id: int
    :param db: The database session.
    :type db: Session
    :return: Updated user.
    :rtype: User
    """
    user = await repository_users.remove_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User id = {user_id} not found")
    return user


@router.patch("/avatar", response_model=UserDB, dependencies=[Depends(RateLimiter(times=1, seconds=120))])
async def patch_avatar(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    Update the current user's avatar.

    :param file: The image file to upload as avatar.
    :type file: UploadFile
    :param current_user: The current user making the request.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: Updated current user's avatar.
    :rtype: User
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    r = cloudinary.uploader.upload(file.file, public_id=f'ContactsApp/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'ContactsApp/{current_user.username}').build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.patch_avatar(current_user, src_url, db)
    return user
