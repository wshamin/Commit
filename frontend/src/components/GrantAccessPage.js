import React, { useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const GrantAccessPage = () => {
    const { trainingId } = useParams();  // Получаем ID тренинга из URL
    const [email, setEmail] = useState('');       // Состояние для поля email

    const grantAccess = async () => {
        try {
            const accessToken = localStorage.getItem('accessToken'); // Получаем токен из localStorage
            const response = await axios.post(
                `/api/trainings/${trainingId}/access/`,
                { user_email: email },
                { headers: { 'Authorization': `Bearer ${accessToken}` } }
            );

            if (response.data.status === 'success') {
                alert(response.data.message);
                // Можно выполнить редирект или обновить страницу, если требуется
            }
        } catch (error) {
            alert(error.response?.data?.detail || "Something went wrong!");
        }
    };

    return (
        <div>
            <input 
                type="email" 
                placeholder="Enter email" 
                value={email} 
                onChange={(e) => setEmail(e.target.value)} 
            />
            <button onClick={grantAccess}>Выдать доступ</button>
        </div>
    );
};

export default GrantAccessPage;
