import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import axios from 'axios';

// Компоненты
import Register from './components/Register';
import Login from './components/Login';
import CreateTraining from './components/CreateTraining';

function Navigation({ isAuthenticated, handleLogout }) {
  return (
    <div>
        {isAuthenticated ? (
            <>
                <Link to="/">
                    <button onClick={handleLogout}>Выход</button>
                </Link>
                <Link to="/create-training">
                    <button>Создать тренинг</button>
                </Link>
            </>
        ) : (
            <>
                <Link to="/register">
                    <button>Регистрация</button>
                </Link>
                <Link to="/login">
                    <button>Вход</button>
                </Link>
            </>
        )}
    </div>
  );
}

async function fetchTrainings() {
    try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}trainings/`);
        return response.data;
    } catch (error) {
        console.error("Ошибка при получении тренингов:", error);
        return [];
    }
}

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [trainings, setTrainings] = useState([]);

    const handleLogout = () => {
        localStorage.removeItem("accessToken");
        setIsAuthenticated(false);
    };

    useEffect(() => {
        setIsAuthenticated(!!localStorage.getItem("accessToken"));
    }, []);

    useEffect(() => {
        async function getTrainings() {
            try {
                const response = fetchTrainings();
                setTrainings(response.data);
            } catch (error) {
                console.error("Ошибка при получении тренингов:", error);
            }
        }

        getTrainings();
    }, []);

    return (
        <Router>
        <div>
            <h1>Welcome to my app</h1>
            <Navigation isAuthenticated={isAuthenticated} handleLogout={handleLogout} />

            <div>
                {trainings.map(training => (
                    <Link to={`/trainings/${training.id}`} style={{
                        display: 'block',
                        width: '30%',  
                        height: '50px',
                        border: '2px solid black',
                        marginBottom: '10px',
                        padding: '10px'
                    }} key={training.id}>
                        <h3>{training.title}</h3>
                        <p>{training.description}</p>
                    </Link>
                ))}
            </div>

            <Routes>
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
            <Route path="/create-training" element={<CreateTraining />} />
            </Routes>
        </div>
        </Router>
    );
}

export default App;
