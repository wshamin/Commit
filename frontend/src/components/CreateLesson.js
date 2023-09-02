import React, { useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import ReactQuill from 'react-quill';  // Редактор для текстового описания
import 'react-quill/dist/quill.snow.css'; // стили для ReactQuill

function CreateLessonPage() {
    const { id: trainingId } = useParams();
    const [lesson, setLesson] = useState({
        title: '',
        video: null,
        description: ''
    });

    const handleVideoUpload = async (event) => {
        const formData = new FormData();
        formData.append("file", event.target.files[0]);
        
        try {
            const response = await axios.post(`${process.env.REACT_APP_API_URL}upload-video/`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setLesson(prevState => ({ ...prevState, video: response.data.video_url }));
        } catch (error) {
            console.error("Ошибка при загрузке видео:", error);
        }
    };

    const handleCreateLesson = async () => {
        try {
            await axios.post(`${process.env.REACT_APP_API_URL}trainings/${trainingId}/lessons/`, {
                title: lesson.title,
                video_url: lesson.video,
                description: lesson.description
            });
            alert("Урок успешно создан!");
        } catch (error) {
            console.error("Ошибка при создании урока:", error);
        }
    };

    return (
        <div>
            <h2>Создать урок</h2>
            <div>
                <label>Название урока:</label>
                <input type="text" value={lesson.title} onChange={e => setLesson(prevState => ({ ...prevState, title: e.target.value }))} />
            </div>
            <div>
                <label>Видео-материалы к уроку:</label>
                <input type="file" onChange={handleVideoUpload} />
            </div>
            <div>
                <label>Текстовое описание урока:</label>
                <ReactQuill 
                    value={lesson.description} 
                    onChange={value => setLesson(prevState => ({ ...prevState, description: value }))} 
                />
            </div>
            <button onClick={handleCreateLesson}>Создать урок</button>
        </div>
    );
}

export default CreateLessonPage;
