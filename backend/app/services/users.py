from typing import List

from bson import ObjectId
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.core.roles import UserRole
from app.core.security import get_password_hash
from app.db.database import user_collection
from app.db.models.users import UserCreate, UserID, UserInDB, UserUpdateAdmin


async def create_user(user: UserCreate) -> UserID:
    user = jsonable_encoder(user)

    user['hashed_password'] = get_password_hash(user['password'])
    del user['password']

    user['role'] = UserRole.USER.value

    new_user = await user_collection.insert_one(user)
    created_user = await user_collection.find_one({'_id': new_user.inserted_id})

    return UserID(**created_user)


async def get_all_users() -> List[UserInDB]:
    users = await user_collection.find().to_list(None)
    return [UserInDB(**user) for user in users]


async def get_single_user(id: str) -> UserInDB:
    if (user := await user_collection.find_one({'_id': ObjectId(id)})) is not None:
        return UserInDB(**user)
    
    raise HTTPException(status_code=404, detail=f'User {id} not found')


async def update_user(id: str, user: UserUpdateAdmin) -> UserInDB:
    # Исключаем пустые значения
    user = {k: v for k, v in dict(user).items() if v is not None}

    if 'password' in user:
        user['hashed_password'] = get_password_hash(user['password'])

    if len(user) >= 1:
        update_result = await user_collection.update_one({'_id': ObjectId(id)}, {'$set': user})

        if update_result.modified_count == 1:
            if (
                updated_user := await user_collection.find_one({'_id': ObjectId(id)})
            ) is not None:
                return UserInDB(**updated_user)

    if (existing_user := await user_collection.find_one({'_id': ObjectId(id)})) is not None:
        return UserInDB(**existing_user)

    raise HTTPException(status_code=404, detail=f'User {id} not found')
