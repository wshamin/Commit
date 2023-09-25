from typing import List

from fastapi import APIRouter, Depends

from ...deps import is_training_owner
from ....core.security import get_current_user
from ....db.database import training_collection, training_access_collection, user_collection
from ....db.models.core import MongoID
from ....db.models.trainings import Training, TrainingBase
from ....db.models.users import User
from ....services.trainings import create_training, delete_training, get_trainings


router = APIRouter()


@router.post('/', response_description='Create new training', response_model=Training)
async def create_training_route(training: TrainingBase, current_user: User = Depends(get_current_user)):
    created_training = await create_training(training, current_user)
    return created_training


@router.get('/', response_description='Get avaliable trainings', response_model=List[Training])
async def get_trainings_route(current_user: User = Depends(get_current_user)):
    trainings = await get_trainings(current_user)
    return trainings


# @router.delete('/', response_description="Delete a training", status_code=204)
# async def delete_training_route(training: MongoID, current_user: User = Depends(get_current_user)):
#     await delete_training(training)
#     return


@router.delete('/', response_description="Delete a training", status_code=204)
async def delete_training_route(training: MongoID, owner: User = Depends(is_training_owner)):
    await delete_training(training)
    return


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
