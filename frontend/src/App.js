import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';

import CreateTraining from './components/CreateTraining/CreateTraining';
import TrainingPage from './components/TrainingPage/TrainingPage';
import Dashboard from './components/Dashboard/Dashboard';
import CreateLesson from './components/CreateLesson/CreateLesson';
import LessonPage from './components/LessonPage/LessonPage';
import GrantAccessPage from './components/GrantAccessPage';
import UsersPage from './components/UserPage';
import TrainingList from './components/TrainingList';
import NavBar from './components/NavBar/NavBar';
import SignIn from './components/SignIn/SignIn';
import SignUp from './components/SignUp/SignUp';

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem("accessToken");
        setIsAuthenticated(!!token);
    }, []);

    return (
        <Router>
            <div>
            <NavBar isAuthenticated={isAuthenticated} setIsAuthenticated={setIsAuthenticated} />
                <Routes>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/users" element={<UsersPage />} />
                    <Route path="/register" element={<SignUp />} />
                    <Route path="/login" element={<SignIn isAuthenticated={isAuthenticated} setIsAuthenticated={setIsAuthenticated} />}/>
                    <Route path="/create-training" element={<CreateTraining />} />
                    <Route path="/trainings/:id" element={<TrainingPage />} />
                    <Route path="/trainings/:trainingId/grant-access/" element={<GrantAccessPage />} />
                    <Route path="/trainings/:id/create-lesson" element={<CreateLesson />} />
                    <Route path="/lessons/:id" element={<LessonPage />} />
                    <Route path="/trainings" element={<TrainingList />} />
                    <Route path="*" element={<Navigate to="/login" />} /> 
                </Routes>
                </div>
        </Router>
    );
}

export default App;