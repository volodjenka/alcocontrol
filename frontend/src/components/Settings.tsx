import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Switch,
  FormControlLabel,
  Alert,
  Snackbar
} from '@mui/material';
import axios from 'axios';

interface Settings {
  daily_limit: number;
  notification_enabled: boolean;
  notification_time: string;
}

const Settings: React.FC = () => {
  const [settings, setSettings] = useState<Settings>({
    daily_limit: 0,
    notification_enabled: true,
    notification_time: '20:00'
  });
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success' as 'success' | 'error'
  });

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await axios.get('/api/settings');
      setSettings(response.data);
    } catch (error) {
      console.error('Error fetching settings:', error);
      setSnackbar({
        open: true,
        message: 'Ошибка при загрузке настроек',
        severity: 'error'
      });
    }
  };

  const handleChange = (field: keyof Settings) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const value = event.target.type === 'checkbox' 
      ? event.target.checked 
      : event.target.value;
    setSettings(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      await axios.post('/api/settings', settings);
      setSnackbar({
        open: true,
        message: 'Настройки успешно сохранены',
        severity: 'success'
      });
    } catch (error) {
      console.error('Error saving settings:', error);
      setSnackbar({
        open: true,
        message: 'Ошибка при сохранении настроек',
        severity: 'error'
      });
    }
  };

  return (
    <Box sx={{ maxWidth: 600, mx: 'auto', mt: 4 }}>
      <Card>
        <CardContent>
          <Typography variant="h5" component="h2" gutterBottom>
            Настройки
          </Typography>
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Дневной лимит (мл)"
              type="number"
              value={settings.daily_limit}
              onChange={handleChange('daily_limit')}
              margin="normal"
            />
            <FormControlLabel
              control={
                <Switch
                  checked={settings.notification_enabled}
                  onChange={handleChange('notification_enabled')}
                />
              }
              label="Включить уведомления"
            />
            <TextField
              fullWidth
              label="Время уведомлений"
              type="time"
              value={settings.notification_time}
              onChange={handleChange('notification_time')}
              margin="normal"
              InputLabelProps={{
                shrink: true,
              }}
              inputProps={{
                step: 300,
              }}
            />
            <Button
              type="submit"
              variant="contained"
              color="primary"
              sx={{ mt: 2 }}
            >
              Сохранить
            </Button>
          </form>
        </CardContent>
      </Card>
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar(prev => ({ ...prev, open: false }))}
      >
        <Alert
          onClose={() => setSnackbar(prev => ({ ...prev, open: false }))}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Settings; 