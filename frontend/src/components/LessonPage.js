// frontend/src/app/components/LessonPage.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

function LessonPage() {
    const { trainingId, lessonId } = useParams();
    const [lesson, setLesson] = useState(null);

    useEffect(() => {
        async function fetchLesson() {
            try {
                const headers = {
                    'Authorization': `Bearer ${localStorage.getItem("accessToken")}`
                };
                const response = await axios.get(`${process.env.REACT_APP_API_URL}trainings/${trainingId}/lessons/${lessonId}`, { headers });
                setLesson(response.data);
            } catch (error) {
                console.error("Ошибка при загрузке урока:", error);
            }
        }

        fetchLesson();
    }, [trainingId, lessonId]);

    return (
        <div>
            {lesson ? (
                <>
                    <h2>{lesson.title}</h2>
                    <video width="100%" controls src={lesson.video_url}></video>
                    <div>{lesson.description}</div>
                </>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
}

export default LessonPage;
