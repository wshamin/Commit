from typing import Dict, Any, List, Union, Optional
from ..db.models import User, UserUpdate
from ..db.database import user_collection


async def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    # Создаем экземпляр модели User для валидации через Pydantic
    user = User(**user_data)

    # Преобразуем модель User обратно в словарь, для корректного присваивания
    # уникального _id в MongoDB
    user_data = user.model_dump(exclude_none=True)

    result = await user_collection.insert_one(user_data)
    new_user_id = result.inserted_id
    new_user = await user_collection.find_one({'_id': new_user_id})
    return new_user


async def get_user_by_id(user_id: str) -> Union[dict, None]:
    user = await user_collection.find_one({'_id': user_id})
    return user


async def get_all_users() -> List[User]:
    users = []
    async for user in user_collection.find():
        users.append(user)
    return users


async def update_user(user_id: str, user_data: Dict[str, Any]) -> Union[dict, None]:
    if not user_data:
        return None
    user_in_db = await user_collection.find_one({'_id': user_id})
    if not user_in_db:
        return None

    user_data = UserUpdate(**user_data).model_dump(exclude_none=True)
    updated_user = await user_collection.update_one({'_id': user_id}, {'$set': user_data})
    if updated_user:
        return await user_collection.find_one({'_id': user_id})
    return None


async def delete_user(user_id: str) -> Union[dict, None]:
    user = await user_collection.find_one({'_id': user_id})
    if user:
        await user_collection.delete_one({'_id': user_id})
        return user
    return None
