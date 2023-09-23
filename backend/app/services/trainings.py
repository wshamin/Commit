from typing import List

from bson import ObjectId
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from ..api.deps import is_training_exist
from ..db.database import training_access_collection, training_collection, user_collection
from ..db.models.core import MongoID
from ..db.models.trainings import TrainingBase, Training, TrainingInDB
from ..db.models.users import User


async def create_training(training: TrainingBase, current_user: User) -> Training:
    training = jsonable_encoder(training)

    training['owner_id'] = current_user.id

    new_training = await training_collection.insert_one(training)
    created_training = await training_collection.find_one({'_id': new_training.inserted_id})

    return Training(**created_training)


async def delete_training(training: MongoID):
    result = await training_collection.delete_one({'_id': training.object_id})

    if result.deleted_count == 1:
        return
    
    raise HTTPException(status_code=404, detail=f'Training {id} not found')


async def get_all_trainings() -> List[TrainingInDB]:
    trainings = await training_collection.find().to_list(None)
    trainings_with_owner_email = []
    
    for training in trainings:
        owner = await user_collection.find_one({'_id': training['owner_id']})
        training['owner_email'] = owner['email']
        trainings_with_owner_email.append(training)
    
    return [TrainingInDB(**training) for training in trainings]


# Получить список тренингов (для отображения на дашборде пользователя)
async def get_trainings(current_user: User) -> List[Training]:
    # Получаем ID тренингов, к которым у пользователя есть доступ или которые принадлежат пользователю
    accessible_trainings_cursor = training_access_collection.find({'user_id': current_user.id})
    owned_trainings_cursor = training_collection.find({'owner_id': current_user.id})

    # Используем set для хранения ID, чтобы избежать дубликатов
    accessible_training_ids = set()

    async for training in accessible_trainings_cursor:
        accessible_training_ids.add(training['training_id'])

    async for training in owned_trainings_cursor:
        accessible_training_ids.add(training['_id'])

    # Запрашиваем все тренинги на основе списка ID
    trainings = await training_collection.find({'_id': {'$in': list(accessible_training_ids)}}).to_list(None)
    return [Training(**training) for training in trainings]
