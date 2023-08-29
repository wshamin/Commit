from fastapi import APIRouter, HTTPException, Depends, status
from bson import ObjectId

from ...db.database import training_collection
from ...db.models import Training, User, Lesson
from ...schema.schemas import trainings_to_dict_list
from ...core.security import get_current_user


router = APIRouter()


@router.get('/trainings/')
async def get_trainings(current_user: User = Depends(get_current_user)):
    trainings = await training_collection.find().to_list(None)
    return trainings_to_dict_list(trainings)


@router.post('/trainings/')
async def create_training(training: Training):
    training_dict = dict(training)

    if training_dict.get('lessons'):
        training_dict['lessons'] = [dict(lesson) for lesson in training.lessons]

    result = await training_collection.insert_one(training_dict)
    if result:
        return {'id': str(result.inserted_id)}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Training creation failed')


@router.get('/trainings/{training_id}/lessons/')
async def get_lessons(training_id: str):
    print(training_id)
    training = await training_collection.find_one({'_id': ObjectId(training_id)})
    if training:
        return training['lessons']
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post('/trainings/{training_id}/lessons/')
async def add_lesson(training_id: str, lesson: Lesson):
    training = await training_collection.find_one({'_id': ObjectId(training_id)})
    if training:
        updated_training = await training_collection.update_one(
            {'_id': ObjectId(training_id)},
            {'$push': {'lessons': dict(lesson)}}
        )
        if updated_training:
            return {'message': 'Lesson added successfully'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
