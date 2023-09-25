from typing import Optional

from pydantic import Field, EmailStr

from ...db.models.core import CustomBaseModel, MongoID, PyObjectId


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

    class Config(TrainingBase.Config):
        schema_extra = {
            'example': {
                'id': '507c7f79bcf86cd7994f6c0e',
                **TrainingBase.Config.schema_extra['example']
            }
        }


class TrainingInDB(Training):
    owner_id: PyObjectId

    class Config(Training.Config):
        schema_extra = {
            'example': {
                **Training.Config.schema_extra['example'],
                'owner_id': '507c7f79bcf86cd7994f6c0e'
            }
        }


class TrainingUpdate(TrainingBase):
    title: Optional[str]
    description: Optional[str]

    class Config(TrainingBase.Config):
        schema_extra = {
            'example': {
                **TrainingBase.Config.schema_extra['example']
            }
        }


class TrainingUpdateAdmin(TrainingUpdate):
    owner_id: Optional[PyObjectId]

    class Config(TrainingUpdate.Config):
        schema_extra = {
            'example': {
                **TrainingUpdate.Config.schema_extra['example'],
                'owner_id': '507c7f79bcf86cd7994f6c0e'
            }
        }
