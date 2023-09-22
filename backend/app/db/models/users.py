from typing import Optional

from pydantic import Field, EmailStr

from ...db.models.core import CustomBaseModel, PyObjectId


class UserBase(CustomBaseModel):
    first_name: str
    last_name: str 
    email: EmailStr 

    class Config(CustomBaseModel.Config):
        schema_extra = {
            'example': {
                'first_name': 'John',
                'last_name': 'Doe',
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
    role: str

    class Config(CustomBaseModel.Config):
        schema_extra = {
            'id': 'string',
            **UserBase.Config.schema_extra['example'],
            'password': 'string',
            'role': 'user'
        }


class UserID(CustomBaseModel):
    id: PyObjectId = Field(alias='_id')
    role: str

    class Config(CustomBaseModel.Config):
        schema_extra = {
            'id': 'string',
            'role': 'user'
        }


class UserUpdate(UserBase):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

    class Config(UserBase.Config):
        schema_extra = {
            **UserBase.Config.schema_extra['example'],
            'password': 'string'
        }


class UserUpdateAdmin(UserUpdate):
    role: Optional[str]

    class Config(CustomBaseModel.Config):
        schema_extra = {
            **UserBase.Config.schema_extra['example'],
            'password': 'string',
            'role': 'user'
        }
