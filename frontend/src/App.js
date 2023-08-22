import React from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';

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
        <Switch>
          <Route exact path="/" component={MyButton} />
          <Route path="/register" component={Register} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
