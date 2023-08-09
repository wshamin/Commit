from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Material(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    filename: str
    filetype: str
    url: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    email: EmailStr
    password: str
    name: str
    role: str
    courses: List[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None
    courses: Optional[List[str]] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Course(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
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
        json_encoders = {ObjectId: str}


class Review(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    course: str
    user: str
    text: str
    rating: int
    response: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
