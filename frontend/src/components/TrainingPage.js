import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import styles from './TrainingPage.module.css';

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
        navigate(`/trainings/${trainingId}/lessons/${lessonId}`);
    };    

    return (
        <div>
            {training ? (
                <>
                    <h2>{training.title}</h2>
                    <p>{training.description}</p>
                    <button onClick={goToCreateLessonPage}>Создать урок</button>
                    {lessons.map(lesson => (
                        <div key={lesson.id} className={styles.lessonBlock} onClick={() => navigateToLesson(lesson.id)}>
                            <h3>{lesson.title}</h3>
                        </div>
                    ))}
                </>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
}

export default TrainingPage;
