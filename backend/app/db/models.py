from typing import List, Optional
from pydantic import Field, BaseModel
import pydantic
import struct
from fastapi.encoders import ENCODERS_BY_TYPE
from bson import ObjectId


class PyObjectId(ObjectId):
    # fix for FastApi/docs
    __origin__ = pydantic.typing.Literal
    __args__ = (str,)

    @property
    def timestamp(self):
        timestamp = struct.unpack(">I", self.binary[0:4])[0]
        return timestamp

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return str(v)


ENCODERS_BY_TYPE[ObjectId] = str
ENCODERS_BY_TYPE[PyObjectId] = str


class Material(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias='_id')
    filename: str
    filetype: str
    url: str


class User(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias='_id')
    email: str
    password: str
    name: str
    role: str
    courses: List[str]


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None
    courses: Optional[List[str]] = None


class Course(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias='_id')
    title: str
    description: str
    materials: List[str]
    cost: float
    owner: ObjectId
    students: List[str]
    reviews: List[str]


class Review(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias='_id')
    course: str
    user: str
    text: str
    rating: int
    response: str

