import axios from 'axios';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
    const [loginData, setLoginData] = useState({
        email: "",
        password: ""
    });

    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setLoginData({
            ...loginData,
            [name]: value
        });
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const dataToSend = `email=${loginData.email}&password=${loginData.password}`;

            const response = await axios.post(`${process.env.REACT_APP_API_URL}token/`, 
            dataToSend, 
                {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                }
            );
            
            localStorage.setItem("accessToken", response.data.access_token);
            navigate("/");
        } catch (error) {
            console.error('Error during login:', error);
            alert('Login failed.');
        }
    };

    return (
        <div>
            <h2>Login Page</h2>
            <form onSubmit={handleLogin}>
                <input type="email" name="email" placeholder="Email" value={loginData.email} onChange={handleChange} required />
                <input type="password" name="password" placeholder="Password" value={loginData.password} onChange={handleChange} required />
                <button type="submit">Вход</button>
            </form>
        </div>
    );
}

export default Login;
