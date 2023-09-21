from fastapi import APIRouter, Body, HTTPException, Depends, status
from bson import ObjectId
from bson.errors import InvalidId
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# from ....db.database import training_collection, lesson_collection
# from ....db.models import Lesson, UserDB
# from ....core.security import get_current_user
# from ...deps import check_training_access


router = APIRouter()

# # Создать урок
# @router.post('/trainings/{training_id}/lessons/', response_description='Create new lesson', response_model=Lesson)
# async def create_lesson(training_id: str, lesson: Lesson = Body(...)):
#     # Проверяем существование тренинга перед добавлением урока
#     training_exists = await training_collection.find_one({'_id': training_id})
#     if not training_exists:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Training not found')
#
#     lesson = jsonable_encoder(lesson)
#     lesson['training_id'] = training_id
#     new_lesson = await lesson_collection.insert_one(lesson)
#     created_lesson = await lesson_collection.find_one({'_id': new_lesson.inserted_id})
#     return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_lesson)
#
#
# # Получить список уроков в тренинге
# @router.get('/trainings/{training_id}/lessons/')
# async def get_lessons(training_id: str, current_user: UserDB = Depends(get_current_user)):
#     # Проверяем, есть ли доступ к тренингу
#     if not await check_training_access(current_user, training_id):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access to lessons denied')
#
#     lessons = await lesson_collection.find({'training_id': training_id}).to_list(None)
#     return lessons_to_dict_list(lessons)
#
#
# # Получить инфу из урока
# @router.get('/lessons/{lesson_id}/', response_model=Lesson)
# async def get_lesson_by_id(lesson_id: str):
#     try:
#         lesson = await lesson_collection.find_one({'_id': lesson_id})
#     except InvalidId:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid lesson ID')
#
#     if lesson:
#         return {**lesson, '_id': lesson['_id']}
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Lesson not found')
