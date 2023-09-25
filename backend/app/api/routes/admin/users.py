from typing import List

from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordBearer

from ....core.security import require_admin_role
from ....db.models.core import PyObjectId
from ....db.models.users import User, UserInDB, UserUpdateAdmin
from ....services.users import delete_user, get_all_users, get_single_user, update_user


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@router.get('/', response_description='Get all users', response_model=List[User])
async def get_all_users_route(current_user: User = Depends(require_admin_role)):
    users = await get_all_users()
    return users


@router.get('/{id}', response_description='Get a single user', response_model=User)
async def get_single_user_route(id: PyObjectId, current_user: User = Depends(require_admin_role)):
    user = await get_single_user(id)
    return user


@router.put('/{id}', response_description='Update a user', response_model=User)
async def update_user_route(
        id: PyObjectId,
        user_updates: UserUpdateAdmin = Body(...),
        current_user: User = Depends(require_admin_role)):
    updated_user = await update_user(id, user_updates)
    return updated_user


@router.delete('/{id}', response_description='Delete a user', status_code=204)
async def delete_user_route(id: PyObjectId, current_user: User = Depends(require_admin_role)):
    await delete_user(id)
    return
