from typing import Dict, Any
from ..db.models import User, Course, Review
from ..db.database import user_collection


async def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    # Создаем экземпляр модели User для валидации через Pydantic
    user = User(**user_data)

    # Преобразуем модель User обратно в словарь, для корректного присваивания
    # уникального _id в MongoDB
    user_data = user.model_dump(exclude_none=True)

    result = await user_collection.insert_one(user_data)
    new_user_id = result.inserted_id
    new_user = await user_collection.find_one({"_id": new_user_id})
    return new_user
