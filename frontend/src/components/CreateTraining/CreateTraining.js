import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import './styles.css';

function CreateTraining() {
    const [trainingData, setTrainingData] = useState({
        title: "",
        description: ""
    });

    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setTrainingData({
            ...trainingData,
            [name]: value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const token = localStorage.getItem('accessToken'); // Используйте тот ключ, под которым вы сохраняете токен в localStorage

            const dataToSend = {
                title: trainingData.title,
                description: trainingData.description
            };
    
            const response = await axios.post(
                `${process.env.REACT_APP_API_URL}trainings/`, 
                dataToSend,
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            );
    
            if (response.status === 201) {
                alert('Тренинг успешно создан!');
                console.log(response);
                navigate(`/trainings/${response.data._id}`);
            } else {
                console.error('Server responded with status:', response.status);
                alert('Произошла ошибка при создании тренинга.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ошибка при создании тренинга.');
        }
    };
    

    return (
        <div className="mainDiv">
            <h2 className="h2Header">Создать тренинг</h2>
            {/* <Box
            component="form"
            sx={{
                '& > :not(style)': { m: 1, width: '25ch' },
            }}
            noValidate
            autoComplete="off"
            >
                <TextField id="outlined-basic" label="Outlined" variant="outlined" />
                <TextField id="filled-basic" label="Filled" variant="filled" />
                <TextField id="standard-basic" label="Standard" variant="standard" />
            </Box>
            <form onSubmit={handleSubmit}>
                <input type="text" name="title" placeholder="Название тренинга" value={trainingData.title} onChange={handleChange} required />
                <textarea name="description" placeholder="Описание тренинга" value={trainingData.description} onChange={handleChange} required />
                <button type="submit">Создать тренинг</button>
            </form> */}
            <Box
            component="form"
            onSubmit={handleSubmit}
            sx={{
                '& > :not(style)': { m: 1, width: '25ch' },
                display: 'flex',
                alignItems: 'flex-start',
                flexDirection: 'column',
            }}
            noValidate
            autoComplete="off"
            >
                <TextField
                    id="outlined-basic"
                    label="Название тренинга"
                    variant="outlined"
                    name="title"
                    value={trainingData.title}
                    onChange={handleChange}
                    required
                />
                <TextField
                    id="filled-basic"
                    label="Описание тренинга"
                    variant="outlined"
                    name="description"
                    value={trainingData.description}
                    onChange={handleChange}
                    required
                />
                <Button variant="contained" type="submit">Создать тренинг</Button>
            </Box>
        </div>
    );
}

export default CreateTraining;
