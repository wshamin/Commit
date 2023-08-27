def user_to_dict(user) -> dict:
    return {
        'id': str(user['_id']),
        'name': user['name'],
        'email': user['email'],
        'role': user['role']
    }


def users_to_dict_list(users) -> list:
    return[user_to_dict(user) for user in users]


def training_to_dict(training) -> dict:
    return {
        'id': str(training['_id']),
        'title': training['title'],
        'description': training['description'],
        'lessons': training['lessons'] if 'lessons' in training else []
    }


def trainings_to_dict_list(trainings) -> list:
    return [training_to_dict(training) for training in trainings]


def lesson_to_dict(lesson) -> dict:
    return {
        'title': lesson['title'],
        'description': lesson['description'],
        'video_url': lesson['video_url'],
        'homework': lesson['homework']
    }


def lessons_to_dict_list(lessons) -> list:
    return [lesson_to_dict(lesson) for lesson in lessons]
