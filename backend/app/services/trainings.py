from typing import List

from fastapi import Body, Depends
from fastapi.encoders import jsonable_encoder

from ..db.database import training_collection, user_collection
from ..db.models.trainings import TrainingBase, TrainingInDB
from ..db.models.users import UserID


async def create_training(training: TrainingBase, current_user: UserID) -> TrainingBase:
    training = jsonable_encoder(training)

    training['owner_id'] = current_user.id

    new_training = await training_collection.insert_one(training)
    created_training = await training_collection.find_one({'_id': new_training.inserted_id})

    return TrainingBase(**created_training)


async def get_all_trainings() -> List[TrainingInDB]:
    trainings = await training_collection.find().to_list(None)
    trainings_with_owner_email = []
    
    for training in trainings:
        owner = await user_collection.find_one({'_id': training['owner_id']})
        training['owner_email'] = owner['email']
        trainings_with_owner_email.append(training)
    
    return [TrainingInDB(**training) for training in trainings]