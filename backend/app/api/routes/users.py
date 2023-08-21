from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ...db.models import UserModel
from ...db.database import user_collection as db

router = APIRouter()


@router.post('/users/', response_description="Add new user", response_model=UserModel)
async def create_new_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    new_user = await db["users"].insert_one(user)
    created_student = await db["users"].find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)
