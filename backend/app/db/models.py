from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from typing import Optional


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
        json_schema_extra = {
            "example": {
                "name": "username",
                "email": "weshamin@gmail.com",
                "password": "test1234",
                "role": "admin",
            }
        }
