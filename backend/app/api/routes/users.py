from datetime import timedelta

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ...core.config import settings
from ...core.security import create_access_token, get_password_hash, verify_password
from ...db.database import user_collection
from ...db.models import Token, User
from ...schema.schemas import users_to_dict_list


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get('/users/')
async def get_users():
    users = await user_collection.find().to_list(None)
    return users_to_dict_list(users)


@router.post('/users/')
async def post_user(user: User):
    user.password = get_password_hash(user.password)
    user_collection.insert_one(dict(user))


@router.post("/token/")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_collection.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    user_obj = User(**user)
    password_verified = verify_password(form_data.password, user_obj.password)
    if not password_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_obj.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.put('/users/{id}')
async def put_user(id: str, user: User):
    user_collection.find_one_and_update({'_id': ObjectId(id)}, {'$set': dict(user)})


@router.delete('/users/{id}')
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    print(user)
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return {"message": "Пользователь удален"}
    else:
        return {"message": "Пользователь не найден"}
