from fastapi import APIRouter
from ...db.models import User
from ...db.database import user_collection
from ...schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()


@router.get('/users/')
async def get_users():
    users = list_serial(user_collection.find())
    return users


@router.post('/users/')
async def post_user(user: User):
    user_collection.insert_one(dict(user))


@router.put('/users/{id}')
async def put_user(id: str, user: User):
    user_collection.find_one_and_update({'_id': ObjectId(id)}, {'$set': dict(user)})


@router.delete('/users/{id}')
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    print(user)
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return {"message": "Student deleted"}
    else:
        return {"message": "Student not found"}
