import * as React from 'react';
import { useNavigate } from 'react-router-dom';

import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';


export default function LessonCard({title, cardId}) {
    const navigate = useNavigate();

    const openCard = () => {
        navigate(`/lessons/${cardId}`);
    }

    return (
        <Box sx={{ width: '50%', marginLeft: '30px', marginTop: '20px' }}>
            <Card sx={{ maxWidth: '462px' }}>
            <CardContent>
                <Typography variant="h5" component="div">
                {title}
                </Typography>
            </CardContent>
            <CardActions>
                <Button onClick={() => openCard(cardId)} size="small">Пройти урок</Button>
            </CardActions>
            </Card>
        </Box>
    );
}