from bson import ObjectId as _ObjectId
from pydantic import BaseModel, Field, EmailStr, field_validator, GetJsonSchemaHandler
from typing import List, Optional, Dict, Any


def check_object_id(value: str) -> str:
    if not _ObjectId.is_valid(value):
        raise ValueError('Invalid ObjectId')
    return value


class PyObjectId(BaseModel):
    @field_validator('check_object_id')
    def validate_object_id(cls, v: str) -> str:
        return check_object_id(cls, v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: Dict[str, Any], handler: GetJsonSchemaHandler
    ) -> Dict[str, Any]:
        json_schema = super().__get_pydantic_json_schema__(core_schema, handler)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(type='string')
        return json_schema


class Material(BaseModel):
    id: PyObjectId = Field(default_factory=_ObjectId, alias='_id')
    filename: str
    filetype: str
    url: str

    class Config:
        populate_by_name = True
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
        populate_by_name = True
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
        populate_by_name = True
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
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {_ObjectId: str}
