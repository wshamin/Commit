from fastapi import APIRouter, HTTPException, Depends, status
from bson import ObjectId
from bson.errors import InvalidId

from ...db.database import training_collection, lesson_collection
from ...db.models import Lesson
from ...schema.schemas import lessons_to_dict_list


router = APIRouter()

# Создать урок
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


# Получить список уроков в тренинге
@router.get('/trainings/{training_id}/lessons/')
async def get_lessons(training_id: str):
    lessons = await lesson_collection.find({'training_id': training_id}).to_list(None)
    return lessons_to_dict_list(lessons)


# Получить инфу из урока
@router.get('/lessons/{lesson_id}/', response_model=Lesson)
async def get_lesson_by_id(lesson_id: str):
    try:
        lesson = await lesson_collection.find_one({'_id': ObjectId(lesson_id)})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid lesson ID")

    if lesson:
        return {**lesson, "_id": str(lesson["_id"])}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")