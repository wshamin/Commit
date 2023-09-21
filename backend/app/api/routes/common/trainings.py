from fastapi import APIRouter, Body, HTTPException, Depends, status
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# from ....db.database import training_collection, training_access_collection, user_collection
# from ....db.models import Training, TrainingAccess, UserDB, PyObjectId, GrantAccessRequest
# from ....schema.schemas import trainings_to_dict_list
# from ....core.security import get_current_user
# from ...deps import is_training_owner


router = APIRouter()


# # Создать тренинг
# @router.post('/trainings/', response_description='Create new training', response_model=Training)
# async def create_training(training: Training = Body(...), current_user: User = Depends(get_current_user)):
#     training = jsonable_encoder(training)
#     training['owner_id'] = str(current_user.id)
#     new_training = await training_collection.insert_one(training)
#     created_training = await training_collection.find_one({'_id': new_training.inserted_id})
#     return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_training)


# # Получить список тренингов (для отображения на дашборде пользователя)
# @router.get('/trainings/')
# async def get_trainings(current_user: User = Depends(get_current_user)):
#     user_id_str = str(current_user.id)

#     # Получаем ID тренингов, к которым у пользователя есть доступ или которые принадлежат пользователю
#     accessible_trainings_cursor = training_access_collection.find({'user_id': user_id_str})
#     owned_trainings_cursor = training_collection.find({'owner_id': user_id_str})

#     # Используем set для хранения ID, чтобы избежать дубликатов
#     accessible_training_ids = set()

#     async for training in accessible_trainings_cursor:
#         accessible_training_ids.add(training['training_id'])

#     async for training in owned_trainings_cursor:
#         accessible_training_ids.add(str(training['_id']))

#     # Запрашиваем все тренинги на основе списка ID
#     trainings = await training_collection.find({'_id': {'$in': list(accessible_training_ids)}}).to_list(None)
#     return trainings_to_dict_list(trainings)


# # Получить материалы из тренинга
# @router.get('/trainings/{training_id}/', response_model=Training)
# async def get_training_by_id(training_id: str):
#     if (training := await training_collection.find_one({'_id': training_id})) is not None:
#         return training
    
#     raise HTTPException(status_code=404, detail=f'Training {id} not found')


# # Выдать доступ к тренингу другому пользователю
# @router.post('/trainings/{training_id}/access/')
# async def grant_access_to_training(
#     training_id: str,
#     request: GrantAccessRequest,
#     current_user: User = Depends(get_current_user)
# ):
#     # Проверяем, что пользователь является владельцем тренинга
#     training = await training_collection.find_one({'_id': training_id})
#     if not training:
#         raise HTTPException(status_code=404, detail='Training not found')
#     if training['owner_id'] != str(current_user.id):
#         raise HTTPException(status_code=403, detail='Not authorized to grant access')

#     # Ищем целевого пользователя по email
#     user_email = request.user_email
#     user = await user_collection.find_one({'email': user_email})
#     if not user:
#         raise HTTPException(status_code=404, detail='User not found')

#     # Проверяем, был ли уже предоставлен доступ целевому пользователю
#     existing_access = await training_access_collection.find_one({
#         'user_id': user['_id'],
#         'training_id': training_id
#     })
#     if existing_access:
#         raise HTTPException(status_code=400, detail='Access already granted')

#     # Выдаем доступ
#     access_record = {'training_id': training_id, 'user_id': user['_id']}
#     await training_access_collection.insert_one(access_record)

#     return {'status': 'success', 'message': f'Access granted to {user_email}'}
