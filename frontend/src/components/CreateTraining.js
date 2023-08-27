import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function CreateTraining() {
    const [trainingData, setTrainingData] = useState({
        title: "",
        description: ""
    });

    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setTrainingData({
            ...trainingData,
            [name]: value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post(`${process.env.REACT_APP_API_URL}trainings/`, trainingData, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem("accessToken")}`,
                    'Content-Type': 'application/json',
                },
            });

            if (response.status === 201) {
                alert('Тренинг успешно создан!');
                navigate(`/trainings/${response.data.id}`);
            } else {
                alert('Произошла ошибка при создании тренинга.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ошибка при создании тренинга.');
        }
    };

    return (
        <div>
            <h2>Создать тренинг</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" name="title" placeholder="Название тренинга" value={trainingData.title} onChange={handleChange} required />
                <textarea name="description" placeholder="Описание тренинга" value={trainingData.description} onChange={handleChange} required />
                <button type="submit">Создать тренинг</button>
            </form>
        </div>
    );
}

export default CreateTraining;