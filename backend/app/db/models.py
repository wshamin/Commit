from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List, Optional


# Создаем обертку для поля _id в MongoDB, т.к. Python не умеет работать с типом данных ObjectId по умолчанию
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class Material(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    filename: str
    filetype: str
    url: str


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    email: str
    password: str
    name: str
    role: str
    courses: List[PyObjectId]


class Course(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    title: str
    description: str
    materials: List[Material]
    cost: float
    owner: PyObjectId
    students: List[PyObjectId]
    reviews: List[PyObjectId]


class Review(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    course: PyObjectId
    user: PyObjectId
    text: str
    rating: int
    response: str
