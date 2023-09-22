from typing import Optional

from pydantic import Field, EmailStr

from ...db.models.core import CustomBaseModel, PyObjectId


class TrainingBase(CustomBaseModel):
    title: str
    description: str 

    class Config(CustomBaseModel.Config):
        schema_extra = {
            'example': {
                'title': 'Training Name Example',
                'description': 'Training Description Example'
            }
        }


class Training(TrainingBase):
    id: PyObjectId = Field(alias='_id')

    class Config(CustomBaseModel.Config):
        schema_extra = {
            'id': 'string'
        }


class TrainingInDB(Training):
    owner_id: PyObjectId

    class Config(CustomBaseModel.Config):
        schema_extra = {
            **TrainingBase.Config.schema_extra['example'],
            'owner_id': 'string',
        }


class TrainingUpdate(TrainingBase):
    title: Optional[str]
    description: Optional[str]

    class Config(TrainingBase.Config):
        schema_extra = {
            **TrainingBase.Config.schema_extra['example']
        }


class TrainingUpdateAdmin(TrainingUpdate):
    owner_id: Optional[PyObjectId]

    class Config(CustomBaseModel.Config):
        schema_extra = {
            **TrainingBase.Config.schema_extra['example'],
            'owner_id': 'string'
        }
