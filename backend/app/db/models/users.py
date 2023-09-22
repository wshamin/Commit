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
        

class User(UserBase):
    id: PyObjectId = Field(alias='_id')
    role: str

    class Config(UserBase.Config):
        schema_extra = {
            **UserBase.Config.schema_extra['example'],
            'id': 'string',
            'role': 'user'
        }


class UserInDB(User):
    hashed_password: str

    class Config(CustomBaseModel.Config):
        schema_extra = {
            **User.Config.schema_extra,
            'hashed_password': 'string'
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
            'role': 'user'
        }
