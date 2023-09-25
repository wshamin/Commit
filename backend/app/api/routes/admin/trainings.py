from typing import List

from fastapi import APIRouter, Body, Depends

from ....core.security import require_admin_role
from ....db.models.core import PyObjectId
from ....db.models.trainings import TrainingInDB, TrainingUpdateAdmin
from ....db.models.users import User
from ....services.trainings import delete_training, get_all_trainings, update_training

router = APIRouter()


@router.get('/', response_description='Get all trainings', response_model=List[TrainingInDB])
async def get_all_trainings_route(current_user: User = Depends(require_admin_role)):
    trainings = await get_all_trainings()
    return trainings


@router.put('/{id}', response_description='Update a user', response_model=TrainingInDB)
async def update_training_route(
        id: PyObjectId,
        training_updates: TrainingUpdateAdmin = Body(...),
        current_user: User = Depends(require_admin_role)):
    updated_training = await update_training(id, training_updates)
    return updated_training


@router.delete('/{id}', response_description="Delete a training", status_code=204)
async def delete_training_route(id: PyObjectId, current_user: User = Depends(require_admin_role)):
    await delete_training(id)
    return
