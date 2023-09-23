from fastapi import HTTPException, status

from ..db.models.trainings import Training
from ..db.models.users import User
from ..db.database import training_collection, training_access_collection


# Функция для проверки является ли пользователь создателем тренинга
async def is_training_exist(training: Training) -> bool:
    training = await training_collection.find_one({'_id': training.id})

    if not training:
        return False
    
    return True


# Функция для проверки является ли пользователь создателем тренинга
async def is_training_owner(training: Training, user: User) -> bool:
    training = await training_collection.find_one({'_id': training.id})
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
