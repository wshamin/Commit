from fastapi import APIRouter, HTTPException, status

from ...db.database import training_collection
from ...db.models import Training

router = APIRouter()

@router.post("/trainings/")
async def create_training(training: Training):
    training_dict = dict(training)

    if not training_dict.get("lessons"):
        training_dict["lessons"] = []

    if training_dict.get("lessons"):
        training_dict["lessons"] = [dict(lesson) for lesson in training.lessons]

    result = await training_collection.insert_one(training_dict)
    if result:
        return {"id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Training creation failed")
