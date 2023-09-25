from fastapi import Depends, HTTPException

from ..db.models.core import PyObjectId
from ..db.models.trainings import Training
from ..db.models.users import User
from ..db.database import training_collection
from ..core.security import get_current_user


async def check_training_owner(training: Training, user: User) -> None:
    if not training['owner_id'] == user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")


# Функция для проверки существует ли тренинг
async def get_training(id: PyObjectId) -> Training:
    training = await training_collection.find_one({'_id': id})

    if not training:
        raise HTTPException(status_code=404, detail=f'Training {id} not found')

    return training


# Функция для проверки является ли пользователь создателем тренинга
async def is_training_owner(id: PyObjectId, user: User = Depends(get_current_user)) -> PyObjectId:
    training = await get_training(id)
    
    await check_training_owner(training, user)
    
    return id


# # Функция для проверки наличия доступа к тренингу
# async def check_training_access(user: User, training_id: str) -> bool:
#     if is_training_owner(user, training_id):
#         return True

#     access = await training_access_collection.find_one({'user_id': str(user.id), 'training_id': training_id})
#     if not access:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No access to this training")
#     return True
