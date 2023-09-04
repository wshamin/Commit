from bson import ObjectId
from pydantic import BaseModel, GetJsonSchemaHandler, Field, EmailStr, root_validator
from pydantic_core import CoreSchema
from typing import Any, Dict, List, Optional


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
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> Dict[str, Any]:
        # Поскольку у родительского класса нет этого метода, мы создаем схему "с нуля"
        return {
            "type": "string",
            "pattern": "^[0-9a-fA-F]{24}$"  # регулярное выражение для ObjectID
        }


def PyObjectIdDecoder(v) -> PyObjectId:
    return PyObjectId(v)


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    role: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_decoders = {ObjectId: PyObjectIdDecoder}
        json_schema_extra = {
            "example": {
                "name": "username",
                "email": "weshamin@gmail.com",
                "password": "test1234",
                "role": "admin",
            }
        }

    @root_validator(pre=True, allow_reuse=True)
    def convert_objectid_to_pyobjectid(cls, values: dict) -> dict:
        if '_id' in values and isinstance(values['_id'], ObjectId):
            values['_id'] = PyObjectId(values['_id'])
        return values


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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class Lesson(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    video_url: str = Field(...)
    training_id: str = None


class Training(BaseModel):
    title: str = Field(...)
    description: str = Field(...)


class TrainingAccess(BaseModel):
    user_id: str = Field(...)
    training_id: str = Field(...)