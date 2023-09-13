import React, { useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';
import ReactQuill from 'react-quill';  // Редактор для текстового описания
import 'react-quill/dist/quill.snow.css'; // стили для ReactQuill
import './styles.css';

function CreateLesson() {
    const { id: trainingId } = useParams();
    const [lesson, setLesson] = useState({
        title: '',
        video: null,
        description: ''
    });

    const navigate = useNavigate();

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
            const response = await axios.post(`${process.env.REACT_APP_API_URL}trainings/${trainingId}/lessons/`, {
                title: lesson.title,
                video_url: lesson.video,
                description: lesson.description
            });
            console.log("Урок успешно создан!");
            navigate(`/lessons/${response.data._id}`);
        } catch (error) {
            console.error("Ошибка при создании урока:", error);
        }
    };

    return (
        <div className="mainDiv">
            <h2>Создать урок</h2>
            <div className="labelDiv">
                <label>Название урока:</label>
                <input type="text" value={lesson.title} onChange={e => setLesson(prevState => ({ ...prevState, title: e.target.value }))} />
            </div>
            <div className="labelDiv">
                <label>Видео-материалы:</label>
                <input type="file" onChange={handleVideoUpload} />
            </div>
            <div className="labelDiv">
                <label>Текстовое описание урока:</label>
                <div className="react-quill-container">
                    <ReactQuill 
                        value={lesson.description} 
                        onChange={value => setLesson(prevState => ({ ...prevState, description: value }))} 
                    />
                </div>
            </div>
            <Button variant="contained" onClick={handleCreateLesson}>Создать урок</Button>
        </div>
    );
}

export default CreateLesson;
