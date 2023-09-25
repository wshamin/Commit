from typing import List

from bson import ObjectId
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.core.roles import UserRole
from app.core.security import get_password_hash
from ..db.models.core import PyObjectId
from app.db.database import user_collection
from app.db.models.users import UserCreate, User, UserInDB, UserUpdateAdmin


async def is_user_exist(email: str) -> bool:
    existing_user = await user_collection.find_one({"email": email})
    return bool(existing_user)


async def create_user(user: UserCreate) -> User:
    user = jsonable_encoder(user)

    if await is_user_exist(user['email']):
        raise HTTPException(status_code=409, detail=f'Email {user.email} is already registered')

    user['hashed_password'] = get_password_hash(user['password'])
    del user['password']

    user['role'] = UserRole.USER

    new_user = await user_collection.insert_one(user)
    created_user = await user_collection.find_one({'_id': new_user.inserted_id})

    return User(**created_user)


async def delete_user(id: PyObjectId):
    result = await user_collection.delete_one({'_id': id})

    if result.deleted_count == 1:
        return

    raise HTTPException(status_code=404, detail=f'User {id} not found')


async def get_all_users() -> List[User]:
    users = await user_collection.find().to_list(None)
    return [User(**user) for user in users]


async def get_single_user(id: PyObjectId) -> User:
    if (user := await user_collection.find_one({'_id': id})) is not None:
        return User(**user)
    
    raise HTTPException(status_code=404, detail=f'User {id} not found')


async def update_user(id: PyObjectId, user_updates: UserUpdateAdmin) -> UserInDB:
    # Исключаем пустые значения
    user_updates = {k: v for k, v in dict(user_updates).items() if v is not None}

    # Если обновляется пароль, то хэшируем и записываем
    if 'password' in user_updates:
        user_updates['hashed_password'] = get_password_hash(user_updates['password'])

    # Если есть изменения инфы о пользователе, то вносим их
    if len(user_updates) >= 1:
        update_result = await user_collection.update_one({'_id': id}, {'$set': user_updates})

        if update_result.modified_count == 1:
            if (
                updated_user := await user_collection.find_one({'_id': id})
            ) is not None:
                return UserInDB(**updated_user)

    # Если нет изменений, то возвращаем полную информацию о пользователе (без пароля)
    if (existing_user := await user_collection.find_one({'_id': id})) is not None:
        return UserInDB(**existing_user)

    # В противном случае кидаем Exception("Пользователь не найден")
    raise HTTPException(status_code=404, detail=f'User {id} not found')
