from typing import Optional

from pydantic import Field, EmailStr

from app.db.models.core import CustomBaseModel, PyObjectId
from ...core.roles import UserRole


class UserBase(CustomBaseModel):
    login: str 
    email: EmailStr 

    class Config(CustomBaseModel.Config):
        schema_extra = {
            'example': {
                'login': 'user',
                'email': 'user@example.com'
            }
        }


class UserCreate(UserBase):
    password: str

    class Config(UserBase.Config):
        schema_extra = {
            **UserBase.Config.schema_extra['example'],
            'password': 'string'
            }


class UserInDB(UserBase):
    id: PyObjectId = Field(alias='_id')
    hashed_password: str
    role: UserRole

    class Config(CustomBaseModel.Config):
        schema_extra = {
            **UserBase.Config.schema_extra['example'],
            'id': 'string',
            'password': 'string',
            'role': 'user'
        }


class UserID(CustomBaseModel):
    id: PyObjectId = Field(alias='_id')
    role: UserRole

    class Config(CustomBaseModel.Config):
        schema_extra = {
            'id': 'string',
            'role': 'user'
        }


class UserUpdate(UserBase):
    login: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

    class Config(UserBase.Config):
        schema_extra = {
            **UserBase.Config.schema_extra['example']
        }


class UserUpdateAdmin(UserUpdate):
    role: Optional[UserRole]

    class Config(CustomBaseModel.Config):
        schema_extra = {
            **UserBase.Config.schema_extra['example'],
            'role': 'user'
        }
