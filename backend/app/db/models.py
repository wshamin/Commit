from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, GetJsonSchemaHandler
from typing import Optional, Dict, Any


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


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    role: str = Field(...)

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
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Viktor Shamin",
                "email": "weshamin@gmail.com",
                "password": "test1234",
                "role": "admin",
            }
        }
