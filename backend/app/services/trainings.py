from typing import List

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from ..db.database import training_access_collection, training_collection
from ..db.models.core import PyObjectId
from ..db.models.trainings import TrainingBase, Training, TrainingInDB, TrainingUpdateAdmin
from ..db.models.users import User


async def create_training(training: TrainingBase, current_user: User) -> Training:
    training = jsonable_encoder(training)

    training['owner_id'] = current_user.id

    new_training = await training_collection.insert_one(training)
    created_training = await training_collection.find_one({'_id': new_training.inserted_id})

    return Training(**created_training)


async def delete_training(id: PyObjectId):
    result = await training_collection.delete_one({'_id': id})

    if result.deleted_count == 1:
        return
    
    raise HTTPException(status_code=404, detail=f'Training {id} not found')


async def get_all_trainings() -> List[TrainingInDB]:
    trainings = await training_collection.find().to_list(None)
    
    return [TrainingInDB(**training) for training in trainings]


# Получить список тренингов (для отображения на дашборде пользователя)
async def get_trainings(current_user: User) -> List[Training]:
    # Получаем ID тренингов, к которым у пользователя есть доступ, или принадлежат пользователю
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


async def update_training(id: PyObjectId, training_updates: TrainingUpdateAdmin) -> TrainingInDB:
    # Исключаем пустые значения
    training_updates = {k: v for k, v in dict(training_updates).items() if v is not None}

    # Если есть изменения в тренинге, то вносим их
    if len(training_updates) >= 1:
        update_result = await training_collection.update_one({'_id': id}, {'$set': training_updates})

        if update_result.modified_count == 1:
            if (
                updated_training := await training_collection.find_one({'_id': id})
            ) is not None:
                return TrainingInDB(**updated_training)

    # Если нет изменений, то возвращаем исходный тренинг
    if (existing_training := await training_collection.find_one({'_id': id})) is not None:
        return TrainingInDB(**existing_training)

    # В противном случае кидаем Exception("Тренинг не найден")
    raise HTTPException(status_code=404, detail=f'Training {id} not found')
