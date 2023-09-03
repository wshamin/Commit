from fastapi import APIRouter, HTTPException, Depends, status
from bson import ObjectId
from bson.errors import InvalidId

from ...db.database import training_collection, lesson_collection
from ...db.models import Training, User, Lesson
from ...schema.schemas import trainings_to_dict_list, lessons_to_dict_list
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


@router.post('/trainings/{training_id}/lessons/')
async def add_lesson(training_id: str, lesson: Lesson):
    # Проверяем существование тренинга перед добавлением урока
    training_exists = await training_collection.find_one({'_id': ObjectId(training_id)})
    if not training_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Training not found")

    lesson_dict = lesson.dict()
    lesson_dict['training_id'] = training_id
    result = await lesson_collection.insert_one(lesson_dict)
    if result:
        return {'id': str(result.inserted_id), 'message': 'Lesson added successfully'}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Lesson creation failed')

@router.get('/trainings/{training_id}/lessons/')
async def get_lessons(training_id: str):
    lessons = await lesson_collection.find({'training_id': training_id}).to_list(None)
    return lessons_to_dict_list(lessons)



