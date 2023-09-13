from datetime import timedelta
from typing import List

from bson import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ...core.config import settings
from ...core.security import create_access_token, get_password_hash, verify_password, require_admin_role, get_current_user
from ...db.database import user_collection
from ...db.models import Token, User, UserCreate, UserUpdate
from ...schema.schemas import users_to_dict_list
from ...core.roles import UserRole


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@router.get('/users/', response_description='List all users', response_model=List[User])
async def list_users(current_user: User = Depends(require_admin_role)):
    users = await user_collection.find().to_list(None)
    return users


@router.post('/users/', response_description='Create new user', response_model=User)
async def create_user(user: UserCreate = Body(...)):
    try:
        user = jsonable_encoder(user)
        user['password'] = get_password_hash(user['password'])
        user['role'] = UserRole.USER.value
        new_user = await user_collection.insert_one(user)
        created_user = await user_collection.find_one({'_id': new_user.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)
    except Exception as e:
        print(f"Error: {e}")
        raise


@router.get('/users/{id}', response_description='Get a single user', response_model=User)
async def show_user(id: str):
    if (user := await user_collection.find_one({'_id': id})) is not None:
        return user
    
    raise HTTPException(status_code=404, detail=f'User {id} not found')


# Обновить все данные о пользователе (включая роль, для администраторов)
@router.put('/users/{id}', response_description='Update a user', response_model=User)
async def update_user(id: str, user: UserUpdate = Body(...), current_user: User = Depends(require_admin_role)):
    user = {k: v for k, v in dict(user).items() if v is not None}

    if 'password' in user:
        user['password'] = get_password_hash(user['password'])

    if len(user) >= 1:
        update_result = await user_collection.update_one({'_id': id}, {'$set': user})

        if update_result.modified_count == 1:
            if (
                updated_user := await user_collection.find_one({'_id': id})
            ) is not None:
                return updated_user

    if (existing_user := await user_collection.find_one({'_id': id})) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f'User {id} not found')


@router.delete('/users/{id}', response_description='Delete a user')
async def delete_user(id: str, current_user: User = Depends(require_admin_role)):
    delete_result = await user_collection.delete_one({'_id': id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f'User {id} not found')


@router.get('/users/current_user/', response_description='Get current user', response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user


@router.post('/token/')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_collection.find_one({'email': form_data.username})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')

    print(user)
    user_obj = User(**user)
    password_verified = verify_password(form_data.password, user_obj.password)
    if not password_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user_obj.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')
