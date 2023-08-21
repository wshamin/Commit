def user_to_dict(user) -> dict:
    return {
        'id': str(user['_id']),
        'name': user['name'],
        'email': user['email'],
        'role': user['role']
    }


def users_to_dict_list(users) -> list:
    return[user_to_dict(user) for user in users]