import axios from 'axios';
import React, { useState } from 'react';

function Register() {
  const [userData, setUserData] = useState({
    name: "",
    email: "",
    password: "",
    role: ""
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUserData({
      ...userData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('${process.env.REACT_APP_API_URL}users/', userData);
      console.log(response.data);
      alert('User registered!');
    } catch (error) {
      console.error('Error registering user:', error);
      alert('Registration failed.');
    }
  };
  
  return (
    <div>
      <h2>Registration Page</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" name="name" placeholder="Name" value={userData.name} onChange={handleChange} required />
        <input type="email" name="email" placeholder="Email" value={userData.email} onChange={handleChange} required />
        <input type="password" name="password" placeholder="Password" value={userData.password} onChange={handleChange} required />
        <input type="text" name="role" placeholder="Role" value={userData.role} onChange={handleChange} required />
        <button type="submit">Регистрация</button>
      </form>
    </div>
  );
}

export default Register;