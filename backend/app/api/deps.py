from bson import ObjectId
from fastapi import HTTPException, status

from ..db.models import User
from ..db.database import training_collection, training_access_collection


# Функция для проверки является ли пользователь создателем тренинга
async def is_training_owner(user: User, training_id: str) -> bool:
    training = await training_collection.find_one({'_id': training_id})
    if not training:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Training not found')
    return str(user.id) == training['owner_id']


# Функция для проверки наличия доступа к тренингу
async def check_training_access(user: User, training_id: str) -> bool:
    if is_training_owner(user, training_id):
        return True

    access = await training_access_collection.find_one({'user_id': str(user.id), 'training_id': training_id})
    if not access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No access to this training")
    return True
