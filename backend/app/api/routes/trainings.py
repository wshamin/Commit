from fastapi import APIRouter, HTTPException, Depends, status

from ...db.database import training_collection
from ...db.models import Training, User
from ...schema.schemas import trainings_to_dict_list
from ...core.security import get_current_user


router = APIRouter()


@router.get('/trainings/')
async def get_trainings(current_user: User = Depends(get_current_user)):
    trainings = await training_collection.find().to_list(None)
    return trainings_to_dict_list(trainings)


@router.post("/trainings/")
async def create_training(training: Training):
    training_dict = dict(training)

    if training_dict.get("lessons"):
        training_dict["lessons"] = [dict(lesson) for lesson in training.lessons]

    result = await training_collection.insert_one(training_dict)
    if result:
        return {"id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Training creation failed")
