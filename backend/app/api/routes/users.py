from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from ...db.models import UserModel
from ...db.database import user_collection as db

router = APIRouter()


@router.post('/users/', response_description="Add new user", response_model=UserModel)
async def create_new_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    new_user = await db["users"].insert_one(user)
    return new_user
