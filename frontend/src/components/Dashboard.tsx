import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Grid,
  CircularProgress,
} from '@mui/material';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';
import axios from 'axios';

interface SoberPeriod {
  id: number;
  start_time: string;
  end_time: string | null;
  is_active: boolean;
}

interface Drink {
  id: number;
  drink_type: string;
  volume: number;
  alcohol_content: number;
  created_at: string;
}

const Dashboard: React.FC = () => {
  const [soberPeriod, setSoberPeriod] = useState<SoberPeriod | null>(null);
  const [recentDrinks, setRecentDrinks] = useState<Drink[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [soberResponse, drinksResponse] = await Promise.all([
        axios.get('/api/sober-periods/active'),
        axios.get('/api/drinks/recent'),
      ]);

      setSoberPeriod(soberResponse.data);
      setRecentDrinks(drinksResponse.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleStartSoberPeriod = async () => {
    try {
      await axios.post('/api/sober-periods/');
      fetchData();
    } catch (error) {
      console.error('Error starting sober period:', error);
    }
  };

  const handleEndSoberPeriod = async () => {
    if (soberPeriod) {
      try {
        await axios.post(`/api/sober-periods/${soberPeriod.id}/end`);
        fetchData();
      } catch (error) {
        console.error('Error ending sober period:', error);
      }
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Текущий статус
          </Typography>
          
          {soberPeriod ? (
            <>
              <Typography variant="body1" gutterBottom>
                Период трезвости начат: {format(new Date(soberPeriod.start_time), 'dd MMMM yyyy HH:mm', { locale: ru })}
              </Typography>
              <Button
                variant="contained"
                color="secondary"
                onClick={handleEndSoberPeriod}
                sx={{ mt: 2 }}
              >
                Завершить период трезвости
              </Button>
            </>
          ) : (
            <>
              <Typography variant="body1" gutterBottom>
                Нет активного периода трезвости
              </Typography>
              <Button
                variant="contained"
                color="primary"
                onClick={handleStartSoberPeriod}
                sx={{ mt: 2 }}
              >
                Начать период трезвости
              </Button>
            </>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Последние записи
          </Typography>
          
          {recentDrinks.length > 0 ? (
            <Grid container spacing={2}>
              {recentDrinks.map((drink) => (
                <Grid item xs={12} key={drink.id}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="body1">
                        {drink.drink_type} - {drink.volume}мл ({drink.alcohol_content}%)
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {format(new Date(drink.created_at), 'dd MMMM yyyy HH:mm', { locale: ru })}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          ) : (
            <Typography variant="body1" color="text.secondary">
              Нет записей о напитках
            </Typography>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default Dashboard; 