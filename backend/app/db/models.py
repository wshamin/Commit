from pydantic import BaseModel, Field
from typing import List, Optional


class Material(BaseModel):
    id: Optional[str] = Field(alias='_id')
    filename: str
    filetype: str
    url: str


class User(BaseModel):
    id: Optional[str] = Field(default=None, alias='_id')
    email: str
    password: str
    name: str
    role: str
    courses: List[str]


class UserUpdate(BaseModel):
    email: Optional[str]
    password: Optional[str]
    name: Optional[str]
    role: Optional[str]
    courses: Optional[List[str]]


class Course(BaseModel):
    id: Optional[str] = Field(alias='_id')
    title: str
    description: str
    materials: List[Material]
    cost: float
    owner: str
    students: List[str]
    reviews: List[str]


class Review(BaseModel):
    id: Optional[str] = Field(alias='_id')
    course: str
    user: str
    text: str
    rating: int
    response: str
