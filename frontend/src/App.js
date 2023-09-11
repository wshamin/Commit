import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';

// Компоненты
import Register from './components/Register';
import Login from './components/Login';
import CreateTraining from './components/CreateTraining';
import TrainingPage from './components/TrainingPage';
import Dashboard from './components/Dashboard';
import CreateLesson from './components/CreateLesson';
import LessonPage from './components/LessonPage';
import GrantAccessPage from './components/GrantAccessPage';
import UsersPage from './components/UserPage';
import TrainingList from './components/TrainingList';

function Navigation({ isAuthenticated, handleLogout }) {
  return (
    <div>
        {isAuthenticated ? (
            <>
                <Link to="/">
                    <button onClick={handleLogout}>Выход</button>
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

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    const handleLogout = () => {
        localStorage.removeItem("accessToken");
        setIsAuthenticated(false);
    };

    useEffect(() => {
        const token = localStorage.getItem("accessToken");
        setIsAuthenticated(!!token);
    }, []);

    return (
        <Router>
            <div>
                <h1>Welcome to my app</h1>
                <Navigation isAuthenticated={isAuthenticated} handleLogout={handleLogout} />

                <Routes>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/users" element={<UsersPage />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
                    <Route path="/create-training" element={<CreateTraining />} />
                    <Route path="/trainings/:id" element={<TrainingPage />} />
                    <Route path="/trainings/:trainingId/grant-access/" element={<GrantAccessPage />} />
                    <Route path="/trainings/:id/create-lesson" element={<CreateLesson />} />
                    <Route path="/lessons/:id" element={<LessonPage />} />
                    <Route path="/trainings" element={<TrainingList />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;