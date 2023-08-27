import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';
import CreateTraining from './components/CreateTraining';

function MyButton({ isAuthenticated, setIsAuthenticated }) {
  return (
    <div>
        {isAuthenticated ? (
            <>
                <Link to="/">
                    <button onClick={() => {
                        localStorage.removeItem("accessToken");
                        setIsAuthenticated(false);
                    }}>
                        Выход
                    </button>
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

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
      const token = localStorage.getItem("accessToken");
      if (token) {
          setIsAuthenticated(true);
      } else {
          setIsAuthenticated(false);
      }
  }, []);

  return (
    <Router>
      <div>
        <h1>Welcome to my app</h1>
        <Routes>
          <Route path="/" element={<MyButton isAuthenticated={isAuthenticated} setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/create-training" element={<CreateTraining />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
