from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, field_validator, GetJsonSchemaHandler
from typing import List, Optional, Dict, Any


class PyObjectId(BaseModel):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: Dict[str, Any], handler: GetJsonSchemaHandler
    ) -> Dict[str, Any]:
        json_schema = super().__get_pydantic_json_schema__(core_schema, handler)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(type='string')
        return json_schema


# class Material(BaseModel):
#     id: PyObjectId = Field(default_factory=ObjectId, alias='_id')
#     filename: str
#     filetype: str
#     url: str
#
#     class Config:
#         populate_by_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    name: str
    email: EmailStr
    password: str
    role: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Viktor Shamin",
                "email": "weshamin@gmail.com",
                "password": "test1234",
                "role": "admin",
            }
        }


class UpdateUserModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    role: Optional[str]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Viktor Shamin",
                "email": "weshamin@gmail.com",
                "password": "test1234",
                "role": "admin",
            }
        }


# class Course(BaseModel):
#     id: PyObjectId = Field(default_factory=ObjectId, alias='_id')
#     title: str
#     description: str
#     materials: List[Material]
#     cost: float
#     owner: str
#     students: List[str]
#     reviews: List[str]
#
#     class Config:
#         populate_by_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#
#
# class Review(BaseModel):
#     id: PyObjectId = Field(default_factory=ObjectId, alias='_id')
#     course: str
#     user: str
#     text: str
#     rating: int
#     response: str
#
#     class Config:
#         populate_by_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
