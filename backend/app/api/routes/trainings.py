from fastapi import APIRouter, HTTPException, status

from ...db.database import training_collection
from ...db.models import Training

router = APIRouter()

@router.post("/trainings/")
async def create_training(training: Training):
    result = training_collection.insert_one(dict(training))
    if result:
        return {"id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Training creation failed")
