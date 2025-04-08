import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  MenuItem,
  Grid,
  Typography,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const drinkTypes = [
  { value: 'beer', label: 'Пиво' },
  { value: 'wine_red', label: 'Красное вино' },
  { value: 'wine_white', label: 'Белое вино' },
  { value: 'wine_sparkling', label: 'Игристое вино' },
  { value: 'vodka', label: 'Водка' },
  { value: 'whiskey', label: 'Виски' },
  { value: 'cognac', label: 'Коньяк' },
  { value: 'rum', label: 'Ром' },
  { value: 'gin', label: 'Джин' },
  { value: 'liqueur', label: 'Ликер' },
  { value: 'cocktail', label: 'Коктейль' },
];

const defaultAlcoholContent = {
  beer: 5,
  wine_red: 13,
  wine_white: 12,
  wine_sparkling: 12,
  vodka: 40,
  whiskey: 40,
  cognac: 40,
  rum: 40,
  gin: 40,
  liqueur: 30,
  cocktail: 20,
};

const DrinkForm: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    drink_type: '',
    volume: '',
    alcohol_content: '',
    price: '',
    location: '',
    mood: '',
    comment: '',
  });

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // Автоматически устанавливаем крепость при выборе типа напитка
    if (name === 'drink_type' && value in defaultAlcoholContent) {
      setFormData((prev) => ({
        ...prev,
        alcohol_content: defaultAlcoholContent[value as keyof typeof defaultAlcoholContent].toString(),
      }));
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      await axios.post('/api/drinks/', {
        ...formData,
        volume: parseFloat(formData.volume),
        alcohol_content: parseFloat(formData.alcohol_content),
        price: formData.price ? parseFloat(formData.price) : null,
      });
      navigate('/');
    } catch (error) {
      console.error('Error adding drink:', error);
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Добавить напиток
        </Typography>
        <Box component="form" onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                select
                fullWidth
                label="Тип напитка"
                name="drink_type"
                value={formData.drink_type}
                onChange={handleChange}
                required
              >
                {drinkTypes.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Объем (мл)"
                name="volume"
                type="number"
                value={formData.volume}
                onChange={handleChange}
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Крепость (%)"
                name="alcohol_content"
                type="number"
                value={formData.alcohol_content}
                onChange={handleChange}
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Цена (опционально)"
                name="price"
                type="number"
                value={formData.price}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Место (опционально)"
                name="location"
                value={formData.location}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Настроение (опционально)"
                name="mood"
                value={formData.mood}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Комментарий (опционально)"
                name="comment"
                multiline
                rows={2}
                value={formData.comment}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
              >
                Добавить
              </Button>
            </Grid>
          </Grid>
        </Box>
      </CardContent>
    </Card>
  );
};

export default DrinkForm; 