from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, TypeVar

T = TypeVar('T')


class User(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    role: str = Field(...)


class UpdateUser(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    role: Optional[str]

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Viktor Shamin",
                "email": "weshamin@gmail.com",
                "password": "test1234",
                "role": "admin",
            }
        }


class Response(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[T] = None
