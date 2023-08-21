from bson import ObjectId as _ObjectId
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Optional


def check_object_id(cls, value: str) -> str:
    if not _ObjectId.is_valid(value):
        raise ValueError('Invalid ObjectId')
    return value


class PyObjectId(str):
    @field_validator("check_object_id", pre=True, each_item=False)
    def validate_object_id(cls, v: str) -> str:
        return check_object_id(cls, v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type='string')
        return field_schema


class Material(BaseModel):
    id: PyObjectId = Field(default_factory=_ObjectId, alias='_id')
    filename: str
    filetype: str
    url: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {_ObjectId: str}


class User(BaseModel):
    id: PyObjectId = Field(default_factory=_ObjectId, alias='_id')
    email: EmailStr
    password: str
    name: str
    role: str
    courses: List[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {_ObjectId: str}


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None
    courses: Optional[List[str]] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {_ObjectId: str}


class Course(BaseModel):
    id: PyObjectId = Field(default_factory=_ObjectId, alias='_id')
    title: str
    description: str
    materials: List[Material]
    cost: float
    owner: str
    students: List[str]
    reviews: List[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {_ObjectId: str}


class Review(BaseModel):
    id: PyObjectId = Field(default_factory=_ObjectId, alias='_id')
    course: str
    user: str
    text: str
    rating: int
    response: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {_ObjectId: str}
