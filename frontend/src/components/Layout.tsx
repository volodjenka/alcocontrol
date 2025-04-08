import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  AppBar,
  BottomNavigation,
  BottomNavigationAction,
  Box,
  Container,
  Paper,
} from '@mui/material';
import {
  Home as HomeIcon,
  Add as AddIcon,
  BarChart as StatsIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const navigationItems = [
    { label: 'Главная', icon: <HomeIcon />, path: '/' },
    { label: 'Добавить', icon: <AddIcon />, path: '/add-drink' },
    { label: 'Статистика', icon: <StatsIcon />, path: '/statistics' },
    { label: 'Настройки', icon: <SettingsIcon />, path: '/settings' },
  ];

  return (
    <Box sx={{ pb: 7 }}>
      <AppBar position="static" color="primary">
        <Container maxWidth="sm">
          <Box sx={{ py: 2 }}>
            AlcoControl
          </Box>
        </Container>
      </AppBar>

      <Container maxWidth="sm" sx={{ mt: 2 }}>
        {children}
      </Container>

      <Paper
        sx={{ position: 'fixed', bottom: 0, left: 0, right: 0 }}
        elevation={3}
      >
        <BottomNavigation
          value={navigationItems.findIndex(item => item.path === location.pathname)}
          onChange={(_, newValue) => {
            navigate(navigationItems[newValue].path);
          }}
          showLabels
        >
          {navigationItems.map((item) => (
            <BottomNavigationAction
              key={item.path}
              label={item.label}
              icon={item.icon}
            />
          ))}
        </BottomNavigation>
      </Paper>
    </Box>
  );
};

export default Layout; 