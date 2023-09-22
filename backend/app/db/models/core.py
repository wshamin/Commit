from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectID")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class CustomBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None


# class Training(BaseModel):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
#     owner_id: Optional[PyObjectId] = None
#     title: str = Field(...)
#     description: str = Field(...)
#
#     class Config:
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#         schema_extra = {
#             "example": {
#                 "owner_id": "64fdbdf67849e5a51f37fa39",
#                 "title": "Training Example",
#                 "description": "Description for training example",
#             }
#         }
#
#
# class TrainingUpdate(BaseModel):
#     owner_id: Optional[PyObjectId]
#     owner_email: Optional[str]
#     title: Optional[str]
#     description: Optional[str]
#
#     class Config:
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#         schema_extra = {
#             "example": {
#                 "owner_id": "64fdbdf67849e5a51f37fa39",
#                 "title": "Training Example",
#                 "description": "Description for training example",
#             }
#         }
#
#
# class TrainingAccess(BaseModel):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
#     user_id: Optional[PyObjectId] = Field(...)
#     training_id: Optional[PyObjectId] = Field(...)
#
#     class Config:
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#
#
# class GrantAccessRequest(BaseModel):
#     user_email: EmailStr
#
#
# class Lesson(BaseModel):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
#     training_id: Optional[PyObjectId] = None
#     title: str = Field(...)
#     description: str = Field(...)
#     video_url: Optional[str]
#
#     class Config:
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#         schema_extra = {
#             "example": {
#                 "title": "Lesson Example",
#                 "description": "Description for lesson example",
#                 "video_url": "URL example",
#             }
#         }
