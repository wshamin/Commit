import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import './styles.css';

const isVideoValid = true;

function LessonPage() {
    const [lesson, setLesson] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const { id: lessonId } = useParams();

    useEffect(() => {
        axios.get(`${process.env.REACT_APP_API_URL}lessons/${lessonId}/`)
            .then(response => {
                setLesson(response.data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Ошибка при получении уроков:", err);
                setError(err);
                setLoading(false);
            });
    }, [lessonId]);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error loading lesson.</p>;
    if (!lesson) return <p>No lesson found.</p>;

    return (
        <div className="mainDiv">
            <h2>{lesson.title}</h2>
            <div
            className="formatted-text"
            dangerouslySetInnerHTML={{ __html: lesson.description }}
            />
            <div className="video">
            <video width="320" height="240" controls>
                <source src={`${process.env.REACT_APP_API_URL}lessons/${lessonId}/video/`} type="video/mp4" />
                Ваш браузер не поддерживает видео тег.
            </video>
            </div>
        </div>
    );
}

export default LessonPage;
