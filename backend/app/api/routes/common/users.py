from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ....core.config import settings
from ....core.security import create_access_token, verify_password
from ....db.database import user_collection
from ....db.models.core import Token
from ....db.models.users import UserCreate, User, UserInDB
from ....services.users import create_user


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@router.post('/', response_description='Create new user', response_model=User)
async def create_user_route(user: UserCreate = Body(...)):
    created_user = await create_user(user)
    return created_user


@router.post('/token/')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_collection.find_one({'email': form_data.username})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')

    user_obj = UserInDB(**user)
    password_verified = verify_password(form_data.password, user_obj.hashed_password)
    if not password_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': str(user_obj.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')
