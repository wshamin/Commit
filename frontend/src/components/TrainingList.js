import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TrainingList = () => {
    const [trainings, setTrainings] = useState([]);
    const [expandedCard, setExpandedCard] = useState(null);

    useEffect(() => {
        fetchTrainings();
    }, []);

    const fetchTrainings = async () => {
    try {
        const headers = {
            'Authorization': `Bearer ${localStorage.getItem("accessToken")}`
        };
        const response = await axios.get(`${process.env.REACT_APP_API_URL}admin/trainings`, { headers });
        setTrainings(response.data);
    } catch (error) {
        console.error(error);
    }
    };

    const handleDelete = async (trainingId) => {
        try {
            const headers = {
                'Authorization': `Bearer ${localStorage.getItem("accessToken")}`
            };
            await axios.delete(`${process.env.REACT_APP_API_URL}admin/trainings/${trainingId}`, { headers });
            fetchTrainings();
        } catch (error) {
            console.error(error);
        }
    };

    const handleExpand = (trainingId) => {
        setExpandedCard(expandedCard === trainingId ? null : trainingId);
    };

    const handleUpdateAuthor = async (trainingId) => {
        try {
            const newOwnerEmail = document.getElementById(`author-email-${trainingId}`).value;
            const headers = {
                'Authorization': `Bearer ${localStorage.getItem("accessToken")}`
            };
            const response = await axios.put(`${process.env.REACT_APP_API_URL}admin/trainings/${trainingId}`, { "owner_email": newOwnerEmail }, { headers });
            if (response.status === 200) {
                alert('Автор изменен');
                fetchTrainings();
            }
        } catch (error) {
            console.error(error);
        }
      };

    return (
        <div>
            {trainings.map((training) => (
                <div
                    style={{
                    display: 'block',
                    width: '30%',
                    height: expandedCard === training._id ? '220px' : '180px',
                    border: '1px solid gray',
                    marginBottom: '10px',
                    marginLeft: '30px',
                    marginTop: '30px',
                    padding: '10px',
                    overflow: 'hidden',
                    transition: 'height 0.3s',
                    }}
                    key={training._id}
                >
                    <h3>{training.title}</h3>
                    <p>{training.description}</p>
                    <p>Автор: {training.owner_email}</p>
                    <button onClick={() => handleDelete(training._id)}>Удалить</button>
                    <button onClick={() => handleExpand(training._id)}>Изменить автора</button>
                    {expandedCard === training._id && (
                    <div>
                        <label htmlFor={`author-email-${training._id}`}>Email автора:</label>
                        <input id={`author-email-${training._id}`} type="email" />
                        <button onClick={() => handleUpdateAuthor(training._id)}>Изменить</button>
                    </div>
                    )}
                </div>
            ))}
      </div>
    );
};

export default TrainingList;