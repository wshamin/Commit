import * as React from 'react';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';
import axios from 'axios';
import TrainingCard from './components/TrainingCard';
import './styles.css';

function Dashboard() {
    const [trainings, setTrainings] = useState([]);
    const [currentUser, setCurrentUser] = useState(null);

    const navigate = useNavigate();

    const handleCreateTrainingClick = () => {
        navigate("/create-training");
      };

    const handleUsersButtonClick = () => {
    navigate("/users");
    };

    const handleTrainingsButtonClick = () => {
        navigate("/trainings");
      };

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

        async function fetchCurrentUser() {
            try {
              const headers = {
                'Authorization': `Bearer ${localStorage.getItem("accessToken")}`
              };
              const response = await axios.get(`${process.env.REACT_APP_API_URL}users/current_user/`, { headers });
              setCurrentUser(response.data);
            } catch (error) {
              console.error("Ошибка при получении текущего пользователя:", error);
            }
          }          

        fetchTrainings();
        fetchCurrentUser();
    }, []);

    return (
            <div>
            <h2 className="h2-header">Личный кабинет</h2>

            <Button variant="contained" onClick={handleCreateTrainingClick} sx={{ marginLeft: '30px' }}>Создать тренинг</Button>

            {currentUser && currentUser.role === 'admin' && (
                <>
                    <Button variant="outlined" onClick={handleUsersButtonClick} sx={{ marginLeft: '20px' }}>Пользователи</Button>
                    <Button variant="outlined" onClick={handleTrainingsButtonClick} sx={{ marginLeft: '20px' }}>Тренинги</Button>
                </>
            )}
            
            <div>
                {trainings.map(card => 
                    <TrainingCard title={card.title} description={card.description} cardId={card.id} />
                )
            }
            </div>
        </div>
    );
}

export default Dashboard;
