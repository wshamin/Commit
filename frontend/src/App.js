import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';

function MyButton() {
  return (
    <Link to="/register">
      <button>
        Register
      </button>
    </Link>
  );
}

function Register() {
  return (
    <div>
      <h2>Registration Page</h2>
      {/* Тут будет форма регистрации */}
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
        </Routes>
      </div>
    </Router>
  );
}

export default App;
