from typing import List

from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordBearer

from ....core.security import require_admin_role
from app.db.models.users import UserID, UserInDB, UserUpdateAdmin
from app.services.users import get_all_users, get_single_user, update_user


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@router.get('/users/', response_description='Get all users', response_model=List[UserInDB])
async def get_all_users_route(current_user: UserID = Depends(require_admin_role)):
    users = await get_all_users()
    return users


@router.get('/users/{id}', response_description='Get a single user', response_model=UserInDB)
async def get_single_user_route(id: str, current_user: UserID = Depends(require_admin_role)):
    user = await get_single_user(id)
    return user


@router.put('/users/{id}', response_description='Update a user', response_model=UserInDB)
async def update_user_route(
        id: str,
        user: UserUpdateAdmin = Body(...),
        current_user: UserID = Depends(require_admin_role)):
    updated_user = await update_user(id, user)
    return updated_user
