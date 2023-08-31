import React from 'react';
import { Link } from 'react-router-dom';

function Dashboard({ trainings }) {
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
