from fastapi import Depends, HTTPException

from ..db.models.core import MongoID
from ..db.models.trainings import Training
from ..db.models.users import User
from ..db.database import training_collection, training_access_collection
from ..core.security import get_current_user


# Функция для проверки существует ли тренинг
async def is_training_exist(training: Training) -> bool:
    training = await training_collection.find_one({'_id': training.id})

    if not training:
        return False
    
    return True


# Функция для проверки является ли пользователь создателем тренинга
async def is_training_owner(training_id: MongoID, user: User = Depends(get_current_user)) -> User:
    training = await training_collection.find_one({'_id': training_id.id})

    if not training:
        raise HTTPException(status_code=404, detail='Training not found')
    
    if not user.id == training_id.id:
        raise HTTPException(sstatus_code=403, detail="Not enough permissions")
    
    return user.id


# # Функция для проверки наличия доступа к тренингу
# async def check_training_access(user: User, training_id: str) -> bool:
#     if is_training_owner(user, training_id):
#         return True

#     access = await training_access_collection.find_one({'user_id': str(user.id), 'training_id': training_id})
#     if not access:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No access to this training")
#     return True
