import axios from 'axios';
import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';

function Login() {
    const [loginData, setLoginData] = useState({
        email: "",
        password: ""
    });

    const history = useHistory();

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
            const response = await axios.post(`${process.env.REACT_APP_API_URL}token/`, {
                username: loginData.email,
                password: loginData.password
            });
            
            localStorage.setItem("accessToken", response.data.access_token);
            history.push("/");  // redirect to home page or dashboard
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
import axios from 'axios';
import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';

function Login() {
    const [loginData, setLoginData] = useState({
        email: "",
        password: ""
    });

    const history = useHistory();

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
            const response = await axios.post(`${process.env.REACT_APP_API_URL}token/`, {
                username: loginData.email,
                password: loginData.password
            });
            
            localStorage.setItem("accessToken", response.data.access_token);
            history.push("/");  // redirect to home page or dashboard
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