from fastapi import APIRouter, HTTPException, Depends, status
from bson import ObjectId
from bson.errors import InvalidId

from ...db.database import training_collection, user_collection
from ...db.models import Training, User
from ...schema.schemas import trainings_to_dict_list, lessons_to_dict_list, user_to_dict
from ...core.security import get_current_user


router = APIRouter()


#CRUD

# Создать тренинг
@router.post('/trainings/')
async def create_training(training: Training):
    training_dict = dict(training)

    result = await training_collection.insert_one(training_dict)
    if result:
        return {'id': str(result.inserted_id)}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Training creation failed')


#Сервисные маршруты


# Получить список тренингов (для отображения на дашборде пользователя)
@router.get('/trainings/')
async def get_trainings(current_user: User = Depends(get_current_user)):
    print(current_user.id)
    trainings = await training_collection.find().to_list(None)
    return trainings_to_dict_list(trainings)


# Получить заголовок и описание тренинга для отображения на странице тренинга
@router.get('/trainings/{training_id}/', response_model=Training)
async def get_training_by_id(training_id: str):
    try:
        training = await training_collection.find_one({'_id': ObjectId(training_id)})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid training ID")

    if training:
        return {**training, "_id": str(training["_id"])} 
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Training not found")
