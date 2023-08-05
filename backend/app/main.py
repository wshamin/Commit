import asyncio
from .services.users_service import (
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user
)


async def run_tests():
    # Создаем пользователя
    test_user_data = {
        "email": "testuser@email.com",
        "password": "securepassword",
        "name": "Test User",
        "role": "user",
        "courses": []
    }
    new_user = await create_user(test_user_data)
    print("Created user:", new_user)

    # Извлекаем всех пользователей
    all_users = await get_all_users()
    print("All users:", all_users)

    # Извлекаем пользователя по ID
    user_id = new_user['_id']
    retrieved_user = await get_user_by_id(user_id)
    print(f"Retrieved user with ID {user_id}:", retrieved_user)

    # Обновляем пользователя
    update_data = {
        "name": "Updated Test User"
    }
    updated_user = await update_user(user_id, update_data)
    print(f"Updated user with ID {user_id}:", updated_user)

    # Удаляем пользователя
    deleted_result = await delete_user(user_id)
    print(f"Deleted user with ID {user_id}:", deleted_result)


def main():
    asyncio.run(run_tests())


if __name__ == "__main__":
    main()
