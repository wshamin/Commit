import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Register from './components/Register';

function MyButton() {
  return (
    <Link to="/register">
      <button>
        Register
      </button>
    </Link>
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
