from fastapi import APIRouter, HTTPException, Depends, status
from bson import ObjectId
from bson.errors import InvalidId

from ...db.database import training_collection, training_access_collection, user_collection
from ...db.models import Training, TrainingResponse, User
from ...schema.schemas import trainings_to_dict_list, lessons_to_dict_list, user_to_dict
from ...core.security import get_current_user


router = APIRouter()


#CRUD

# Создать тренинг
@router.post('/trainings/', response_model=TrainingResponse)
async def create_training(training: Training, current_user: User = Depends(get_current_user)):
    training_to_insert = training.dict()
    training_to_insert["owner_id"] = current_user.id

    result = await training_collection.insert_one(training_to_insert)
    if result:
        return {'id': str(result.inserted_id)}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Training creation failed')


#Сервисные маршруты


# Получить список тренингов (для отображения на дашборде пользователя)
@router.get('/trainings/')
async def get_trainings(current_user: User = Depends(get_current_user)):
    # Получить список всех тренингов, к которым у пользователя есть доступ
    accessible_trainings = await training_access_collection.find({'user_id': current_user.id}).to_list(None)
    accessible_training_ids = [training['training_id'] for training in accessible_trainings]

    # Включить тренинги, которые принадлежат пользователю
    owned_trainings = await training_collection.find({'owner_id': current_user.id}).to_list(None)
    for training in owned_trainings:
        if str(training['_id']) not in accessible_training_ids:
            accessible_training_ids.append(str(training['_id']))

    trainings = await training_collection.find({'_id': {'$in': [ObjectId(id) for id in accessible_training_ids]}}).to_list(None)
    return trainings_to_dict_list(trainings)


# Получить заголовок и описание тренинга для отображения на странице тренинга
@router.get('/trainings/{training_id}/', response_model=Training)
async def get_training_by_id(training_id: str):
    try:
        training = await training_collection.find_one({'_id': ObjectId(training_id)})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid training ID')

    if training:
        return {**training, '_id': str(training['_id'])} 
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Training not found')
