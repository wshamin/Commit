import os

from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

# Директория для сохранения видео
VIDEOS_DIR = "uploaded_videos"
os.makedirs(VIDEOS_DIR, exist_ok=True)

@router.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    try:
        # Создание пути к файлу с использованием его имени
        file_path = os.path.join(VIDEOS_DIR, file.filename)

        # Запись файла
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        return {"video_url": file.filename, "message": "Video uploaded successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Video upload error: {e}")