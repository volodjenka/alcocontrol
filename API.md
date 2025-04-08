# API Документация AlcoControl

## Базовый URL

```
https://api.alcocontrol.com/v1
```

## Аутентификация

Все запросы к API должны включать токен в заголовке:

```
Authorization: Bearer <token>
```

## Endpoints

### Пользователи

#### Регистрация

```http
POST /users/register
```

Request body:
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "telegram_id": "string"
}
```

Response:
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "telegram_id": "string",
  "created_at": "datetime"
}
```

#### Авторизация

```http
POST /users/login
```

Request body:
```json
{
  "email": "string",
  "password": "string"
}
```

Response:
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "expires_in": "integer"
}
```

### Напитки

#### Получение списка напитков

```http
GET /drinks
```

Query parameters:
- `user_id` (integer, optional)
- `limit` (integer, optional)
- `offset` (integer, optional)

Response:
```json
{
  "items": [
    {
      "id": "integer",
      "name": "string",
      "type": "string",
      "volume": "float",
      "alcohol_content": "float",
      "user_id": "integer",
      "created_at": "datetime"
    }
  ],
  "total": "integer",
  "limit": "integer",
  "offset": "integer"
}
```

#### Создание напитка

```http
POST /drinks
```

Request body:
```json
{
  "name": "string",
  "type": "string",
  "volume": "float",
  "alcohol_content": "float"
}
```

Response:
```json
{
  "id": "integer",
  "name": "string",
  "type": "string",
  "volume": "float",
  "alcohol_content": "float",
  "user_id": "integer",
  "created_at": "datetime"
}
```

#### Обновление напитка

```http
PUT /drinks/{id}
```

Request body:
```json
{
  "name": "string",
  "type": "string",
  "volume": "float",
  "alcohol_content": "float"
}
```

Response:
```json
{
  "id": "integer",
  "name": "string",
  "type": "string",
  "volume": "float",
  "alcohol_content": "float",
  "user_id": "integer",
  "created_at": "datetime"
}
```

#### Удаление напитка

```http
DELETE /drinks/{id}
```

Response: 204 No Content

### Статистика

#### Получение статистики

```http
GET /stats
```

Query parameters:
- `user_id` (integer, required)
- `start_date` (date, optional)
- `end_date` (date, optional)

Response:
```json
{
  "total_drinks": "integer",
  "total_volume": "float",
  "total_alcohol": "float",
  "drinks_by_type": {
    "beer": "integer",
    "wine": "integer",
    "spirits": "integer"
  },
  "daily_stats": [
    {
      "date": "date",
      "count": "integer",
      "volume": "float",
      "alcohol": "float"
    }
  ]
}
```

### Telegram Bot

#### Отправка сообщения

```http
POST /telegram/send
```

Request body:
```json
{
  "user_id": "integer",
  "message": "string"
}
```

Response:
```json
{
  "success": "boolean",
  "message_id": "integer"
}
```

## Коды ошибок

- 400 Bad Request - Неверный запрос
- 401 Unauthorized - Не авторизован
- 403 Forbidden - Доступ запрещен
- 404 Not Found - Ресурс не найден
- 422 Unprocessable Entity - Ошибка валидации
- 500 Internal Server Error - Внутренняя ошибка сервера

## Ограничения

- Rate limit: 100 запросов в минуту
- Максимальный размер запроса: 1MB
- Токен действителен 24 часа

## Версионирование

API использует семантическое версионирование. Текущая версия API - v1.

## Поддержка

По вопросам API обращайтесь:
- Email: api-support@alcocontrol.com
- Telegram: @alcocontrol_support 