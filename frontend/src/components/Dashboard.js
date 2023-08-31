import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function Dashboard() {
    const [trainings, setTrainings] = useState([]);

    useEffect(() => {
        async function fetchTrainings() {
            try {
                const headers = {
                    'Authorization': `Bearer ${localStorage.getItem("accessToken")}`
                };
                const response = await axios.get(`${process.env.REACT_APP_API_URL}trainings/`, { headers });
                setTrainings(response.data);
            } catch (error) {
                console.error("Ошибка при получении тренингов:", error);
            }
        }

        fetchTrainings();
    }, []);

    return (
        <div>
            <h2>Личный кабинет</h2>
            <Link to="/create-training">
                <button>Создать тренинг</button>
            </Link>

            <div>
                {trainings.map(training => (
                    <Link to={`/trainings/${training.id}`} style={{
                        display: 'block',
                        width: '30%',
                        height: '150px',
                        border: '2px solid black',
                        marginBottom: '10px',
                        marginLeft: '30px',
                        padding: '10px'
                    }} key={training.id}>
                        <h3>{training.title}</h3>
                        <p>{training.description}</p>
                    </Link>
                ))}
            </div>
        </div>
    );
}

export default Dashboard;
