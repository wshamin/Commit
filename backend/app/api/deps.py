from bson import ObjectId
from fastapi import HTTPException, status

from .routes.trainings import training_collection
from .routes.lessons import lesson_collection
from ..db.models import User
from ..db.database import training_access_collection

async def check_training_access(user: User, training_id: str) -> bool:
    # Проверяем, является ли пользователь владельцем тренинга
    training = await training_collection.find_one({'_id': training_id})
    if not training:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Training not found')
    
    if str(user.id) == training.get('owner_id'):
        return True

    # Проверяем, есть ли у пользователя доступ к тренингу
    access = await training_access_collection.find_one({'user_id': str(user.id), 'training_id': training_id})
    if access:
        return True

    return False
