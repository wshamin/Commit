import os

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from bson import ObjectId

from ....db.database import lesson_collection

router = APIRouter()

# Директория для видео
VIDEOS_DIR = 'uploaded_videos'
os.makedirs(VIDEOS_DIR, exist_ok=True)

# Загрузка видео
@router.post('/upload-video/')
async def upload_video(file: UploadFile = File(...)):
    try:
        # Создание пути к файлу с использованием его имени
        file_path = os.path.join(VIDEOS_DIR, file.filename)

        # Запись файла
        with open(file_path, 'wb') as buffer:
            buffer.write(file.file.read())

        return {'video_url': file.filename, 'message': 'Video uploaded successfully!'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Video upload error: {e}')


# Получить видео
@router.get('/lessons/{lesson_id}/video/')
async def get_video(lesson_id: str):
    lesson = await lesson_collection.find_one({'_id': lesson_id})
    if not lesson:
        raise HTTPException(status_code=404, detail=f'Lesson {id} not found')

    video_path = os.path.join(VIDEOS_DIR, lesson['video_url'])
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail='Video not found')

    return FileResponse(video_path)
