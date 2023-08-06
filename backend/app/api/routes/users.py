from fastapi import APIRouter, HTTPException, Body

from ...services.users_service import (
    create_user,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user
)

from ...db.models import User, UserUpdate

router = APIRouter()


@router.post('/users/', response_model=User)
async def create_new_user(user: User = Body(...)):
    user_data = user.model_dump(exclude_unset=True)
    new_user = await create_user(user_data)
    return new_user


@router.get('/users/{user_id}', response_model=User)
async def get_single_user(user_id: str):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.get('/users/', response_model=list[User])
async def get_users_list():
    return await get_all_users()


@router.put('/users/{user_id}', response_model=User)
async def modify_user(user_id: str, user: UserUpdate = Body(...)):
    user_updated = await update_user(user_id, user.model_dump(exclude_unset=True))
    if not user_updated:
        raise HTTPException(status_code=404, detail='User not found')
    return user_updated


@router.delete('/users/{user_id}', response_model=User)
async def remove_user(user_id: str):
    deleted_user = await delete_user(user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail='User not found')
    return deleted_user
