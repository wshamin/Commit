from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from ...db.models import UserModel, UpdateUserModel
from ...db.database import user_collection as db

app = APIRouter()


@app.post('/users/', response_description="Add new user", response_model=UserModel)
async def create_new_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    new_user = await db["students"].insert_one(user)
    return new_user
