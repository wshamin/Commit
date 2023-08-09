from typing import List, Optional
from typing_extensions import Annotated
from pydantic import Field, BaseModel
from pydantic.functional_validators import AfterValidator
from bson import ObjectId as _ObjectId


def check_object_id(value: str) -> str:
    if not _ObjectId.is_valid(value):
        raise ValueError('Invalid ObjectId')
    return value


ObjectId = Annotated[str, AfterValidator(check_object_id)]


class Material(BaseModel):
    id: Optional[ObjectId] = Field(alias='_id')
    filename: str
    filetype: str
    url: str


class User(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias='_id')
    email: str
    password: str
    name: str
    role: str
    courses: List[ObjectId]


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None
    courses: Optional[List[ObjectId]] = None


class Course(BaseModel):
    id: Optional[ObjectId] = Field(alias='_id')
    title: str
    description: str
    materials: List[Material]
    cost: float
    owner: ObjectId
    students: List[ObjectId]
    reviews: List[ObjectId]


class Review(BaseModel):
    id: Optional[ObjectId] = Field(alias='_id')
    course: ObjectId
    user: ObjectId
    text: str
    rating: int
    response: str

