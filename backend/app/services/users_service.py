from typing import Dict, Any
from backend.app.db.models import User, Course, Review
from backend.app.db.database import user_collection


async def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    user = User(**user_data)
    # Создаем ключи в словаре согласно алиасам с помощью by_alias=True.
    # Это позволяет возвращаемому словарю использовать _id в качестве ключа для значения id,
    # т.к. в MongoDB у каждого документа есть значение _id.
    result = await user_collection.insert_one(user.model_dump(by_alias=True))
    new_user = await user_collection.find_one({'_id': result.inserted_id})
    return new_user
