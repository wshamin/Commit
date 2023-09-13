import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { grey, blue } from '@mui/material/colors';

const defaultTheme = createTheme({
    palette: {
      primary: blue,
      secondary: grey,
    }});

function NavBar({ isAuthenticated, setIsAuthenticated }) {
  const navigate = useNavigate();

  const handleLogin = () => {
    navigate("/login");
  };

  const handleRegister = () => {
    navigate("/register");
  };

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    setIsAuthenticated(false);
    navigate("/login");
  };

  const hanldeBreadButton = () => {
    navigate("/");
  }

  return (
    <ThemeProvider theme={defaultTheme}>
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }} onClick={hanldeBreadButton}>
            Commit
          </Typography>
          {!isAuthenticated ? (
              <>
                <Button color="inherit" onClick={handleLogin}>Вход</Button>
                <Button color="inherit" onClick={handleRegister}>Регистрация</Button>
              </>
            ) : (
              <Button color="inherit" onClick={handleLogout}>Выход</Button>
            )}
        </Toolbar>
      </AppBar>
    </Box>
    </ThemeProvider>
  );
}

export default NavBar;