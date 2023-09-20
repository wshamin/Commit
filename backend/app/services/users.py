from datetime import timedelta
from typing import List

from bson import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..core.config import settings
from ..core.security import create_access_token, get_password_hash, verify_password, require_admin_role, get_current_user
from ..db.database import user_collection
from ..db.models import Token, UserDB, UserCreate, UserRead
from ..core.roles import UserRole


async def get_all_users():
    users = await user_collection.find().to_list(None)
    return [UserRead(**user) for user in users]


async def create_user(user: UserCreate):
    user = jsonable_encoder(user)
    user['password'] = get_password_hash(user['password'])
    user['role'] = UserRole.USER.value

    new_user = await user_collection.insert_one(user)
    created_user = await user_collection.find_one({'_id': new_user.inserted_id})

    del created_user['password']
    print(created_user)

    return UserRead(**created_user)