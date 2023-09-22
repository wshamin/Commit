from typing import List

from fastapi import APIRouter, Depends

from ....core.security import require_admin_role
from ....db.models.trainings import TrainingInDB
from ....db.models.users import UserID
from ....services.trainings import get_all_trainings

router = APIRouter()


@router.get('/trainings/', response_description='Get all trainings', response_model=List[TrainingInDB])
async def get_all_trainings_route(current_user: UserID = Depends(require_admin_role)):
    trainings = await get_all_trainings()
    return trainings


# @router.put('/admin/trainings/{id}', response_description='Update a training', response_model=Training)
# async def update_training(id: str, training: TrainingUpdate = Body(...), current_user: User = Depends(require_admin_role)):
#     training_dict = training.dict(exclude_unset=True)

#     if 'owner_email' in training_dict:
#         owner = await user_collection.find_one({'email': training_dict['owner_email']})
#         if owner:
#             training_dict['owner_id'] = str(owner['_id'])
#         else:
#             raise HTTPException(status_code=400, detail=f'User with email {training_dict["owner_email"]} not found')
#         del training_dict['owner_email']

#     if len(training_dict) >= 1:
#         update_result = await training_collection.update_one({'_id': id}, {'$set': training_dict})

#         if update_result.modified_count == 1:
#             if (
#                 updated_training := await training_collection.find_one({'_id': id})
#             ) is not None:
#                 return updated_training

#     if (existing_training := await training_collection.find_one({'_id': id})) is not None:
#         return existing_training

#     raise HTTPException(status_code=404, detail=f'Training {id} not found')


# @router.delete('/admin/trainings/{training_id}', response_description='Delete training', response_model=dict)
# async def delete_training(training_id: str, current_user: User = Depends(require_admin_role)):
#     training = await training_collection.find_one({'_id': training_id})
#     if not training:
#         raise HTTPException(status_code=404, detail='Training not found')
#     await training_collection.delete_one({'_id': training_id})
#     return {'message': 'Training deleted successfully'}
