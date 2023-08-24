import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';

function MyButton() {
  return (
    <div>
      <Link to="/register">
        <button>
          Регистрация
        </button>
      </Link>
      
      <Link to="/login">
        <button>
          Вход
        </button>
      </Link>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div>
        <h1>Welcome to my app</h1>
        <Routes>
          <Route path="/" element={<MyButton />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
