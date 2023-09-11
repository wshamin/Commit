from typing import List
from fastapi import APIRouter, Depends

from ....core.security import require_admin_role
from ....db.database import training_collection
from ....db.models import Training, User
from ....schema.schemas import trainings_to_dict_list


router = APIRouter()


@router.get('/admin/trainings/', response_description='Get all trainings', response_model=List[Training])
async def get_all_trainings(current_user: User = Depends(require_admin_role)):
    trainings = await training_collection.find().to_list(None)
    return trainings_to_dict_list(trainings)
