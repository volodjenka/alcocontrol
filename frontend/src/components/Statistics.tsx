import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  CircularProgress,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Line, Bar, Pie } from 'react-chartjs-2';
import { format, subDays, startOfWeek, endOfWeek } from 'date-fns';
import { ru } from 'date-fns/locale';
import axios from 'axios';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

interface DrinkStats {
  total_drinks: number;
  total_volume: number;
  total_alcohol: number;
  total_spent: number;
  drinks_by_type: { [key: string]: number };
  drinks_by_day: { [key: string]: number };
}

const Statistics: React.FC = () => {
  const [period, setPeriod] = useState('week');
  const [stats, setStats] = useState<DrinkStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, [period]);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`/api/statistics?period=${period}`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching statistics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !stats) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  const drinksByTypeData = {
    labels: Object.keys(stats.drinks_by_type).map(type => {
      const types: { [key: string]: string } = {
        beer: 'Пиво',
        wine_red: 'Красное вино',
        wine_white: 'Белое вино',
        wine_sparkling: 'Игристое вино',
        vodka: 'Водка',
        whiskey: 'Виски',
        cognac: 'Коньяк',
        rum: 'Ром',
        gin: 'Джин',
        liqueur: 'Ликер',
        cocktail: 'Коктейль',
      };
      return types[type] || type;
    }),
    datasets: [
      {
        data: Object.values(stats.drinks_by_type),
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF',
          '#FF9F40',
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF',
        ],
      },
    ],
  };

  const drinksByDayData = {
    labels: Object.keys(stats.drinks_by_day).map(date =>
      format(new Date(date), 'dd MMM', { locale: ru })
    ),
    datasets: [
      {
        label: 'Количество напитков',
        data: Object.values(stats.drinks_by_day),
        borderColor: '#2196f3',
        backgroundColor: 'rgba(33, 150, 243, 0.5)',
      },
    ],
  };

  return (
    <Box>
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} sm={6}>
              <Typography variant="h6">Статистика</Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Период</InputLabel>
                <Select
                  value={period}
                  label="Период"
                  onChange={(e) => setPeriod(e.target.value)}
                >
                  <MenuItem value="week">Неделя</MenuItem>
                  <MenuItem value="month">Месяц</MenuItem>
                  <MenuItem value="year">Год</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Общая информация
              </Typography>
              <Typography variant="body1">
                Всего напитков: {stats.total_drinks}
              </Typography>
              <Typography variant="body1">
                Общий объем: {stats.total_volume} мл
              </Typography>
              <Typography variant="body1">
                Общее количество алкоголя: {stats.total_alcohol.toFixed(1)} мл
              </Typography>
              <Typography variant="body1">
                Потрачено: {stats.total_spent.toFixed(2)} ₽
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Распределение по типам
              </Typography>
              <Box sx={{ height: 300 }}>
                <Pie data={drinksByTypeData} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Динамика потребления
              </Typography>
              <Box sx={{ height: 300 }}>
                <Bar data={drinksByDayData} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Statistics; 