import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { TelegramWebApp } from '@twa-dev/sdk';

// Компоненты
import Dashboard from './components/Dashboard';
import DrinkForm from './components/DrinkForm';
import Statistics from './components/Statistics';
import Settings from './components/Settings';
import Layout from './components/Layout';

// Создаем тему
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#2196f3',
    },
    secondary: {
      main: '#f50057',
    },
  },
});

function App() {
  React.useEffect(() => {
    // Инициализация Telegram WebApp
    TelegramWebApp.ready();
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/add-drink" element={<DrinkForm />} />
            <Route path="/statistics" element={<Statistics />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  );
}

export default App; 