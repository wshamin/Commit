import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import Button from '@mui/material/Button';
import LessonCard from './components/LessonCard';
import './styles.css';

function TrainingPage() {
    const [training, setTraining] = useState(null);
    const [lessons, setLessons] = useState([]);
    const navigate = useNavigate();

    const { id: trainingId } = useParams();

    useEffect(() => {
        async function fetchTraining() {
            try {
                const headers = {
                    'Authorization': `Bearer ${localStorage.getItem("accessToken")}`
                };
                const trainingResponse = await axios.get(`${process.env.REACT_APP_API_URL}trainings/${trainingId}/`, { headers });
                const trainingData = trainingResponse.data;
                
                const lessonsResponse = await axios.get(`${process.env.REACT_APP_API_URL}trainings/${trainingId}/lessons/`, { headers });
                const lessonsData = lessonsResponse.data;
    
                setTraining(trainingData);
                setLessons(lessonsData);
            } catch (error) {
                console.error("Ошибка при загрузке данных о тренинге:", error);
            }
        }
        fetchTraining();
    }, [trainingId]);

    // Функция для перехода на страницу создания урока
    const goToCreateLessonPage = () => {
        navigate(`/trainings/${trainingId}/create-lesson`);
    };

    // Функция для перехода на страницу урока
    const navigateToLesson = (lessonId) => {
        navigate(`/lessons/${lessonId}`);
    };    

    // Функция для перехода на страницу выдачи доступа
    const goToGrantAccessPage = () => {
        navigate(`/trainings/${trainingId}/grant-access/`);
    };    

    return (
        <div>
            {training ? (
                <>
                    <h2 className="h2-header">{training.title}</h2>
                    <p className="p-text">{training.description}</p>
                    <Button variant="contained" onClick={goToCreateLessonPage} sx={{ marginLeft: '30px' }}>Создать урок</Button>
                    <Button variant="contained" onClick={goToGrantAccessPage} sx={{ marginLeft: '20px' }}>Выдать доступ</Button>
                    <div>
                        {lessons.map(card => 
                            <LessonCard title={card.title} cardId={card.id} />
                        )
                        }
                    </div>
                </>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
}

export default TrainingPage;
