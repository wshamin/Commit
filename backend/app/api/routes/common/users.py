from datetime import timedelta
# from typing import List

from bson import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ....core.config import settings
from ....core.security import create_access_token, get_password_hash, verify_password, require_admin_role, get_current_user
from ....db.database import user_collection
from ....db.models.core import Token
from ....db.models.users import UserCreate, UserID, UserInDB
# from ....core.roles import UserRole
from ....services.users import check_existing_user, create_user


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@router.post('/users/', response_description='Create new user', response_model=UserID)
async def create_user_route(user: UserCreate = Body(...)):
    if await check_existing_user(user.email):
        raise HTTPException(status_code=400, detail="Email already exists")

    created_user = await create_user(user)
    return created_user
#
#
# @router.get('/users/{id}', response_description='Get a current user', response_model=UserRead)
# async def get_current_user(id: str, current_user: UserRead = Depends(require_admin_role)):
#     user = await get_single_user(id)
#     return user
#
#
# @router.delete('/users/{id}', response_description='Delete a user')
# async def delete_user(id: str, current_user: UserRead = Depends(require_admin_role)):
#     delete_result = await user_collection.delete_one({'_id': id})
#
#     if delete_result.deleted_count == 1:
#         return Response(status_code=status.HTTP_204_NO_CONTENT)
#
#     raise HTTPException(status_code=404, detail=f'User {id} not found')
#
#
# @router.get('/users/current_user/', response_description='Get current user', response_model=UserRead)
# async def get_current_user_info(current_user: UserRead = Depends(get_current_user)):
#     return current_user
#
#


@router.post('/token/')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_collection.find_one({'email': form_data.username})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')

    user_obj = UserInDB(**user)
    password_verified = verify_password(form_data.password, user_obj.hashed_password)
    if not password_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': str(user_obj.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')
