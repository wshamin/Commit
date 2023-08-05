import asyncio
from backend.app.services.users_service import create_user


def main():
    test_user_data = {
        "email": "testuser@email.com",
        "password": "securepassword",
        "name": "Test User",
        "role": "user",
        "courses": []
    }

    new_user = asyncio.run(create_user(test_user_data))
    print(new_user)


if __name__ == "__main__":
    main()
