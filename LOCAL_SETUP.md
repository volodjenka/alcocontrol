# Локальный запуск AlcoControl

## Предварительные требования

1. Python 3.9+
2. Node.js 16+
3. PostgreSQL
4. Telegram Bot Token (получить у @BotFather)

## Настройка базы данных

1. Создайте базу данных PostgreSQL:
```bash
psql -U postgres
CREATE DATABASE alcocontrol;
\q
```

2. Примените миграции:
```bash
alembic upgrade head
```

## Настройка бэкенда

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Запустите бэкенд:
```bash
uvicorn app.main:app --reload
```

## Настройка фронтенда

1. Перейдите в директорию фронтенда:
```bash
cd frontend
```

2. Установите зависимости:
```bash
npm install
```

3. Запустите фронтенд:
```bash
npm start
```

## Настройка Telegram бота

1. Получите токен бота у @BotFather в Telegram
2. Добавьте токен в файл `.env`:
```
TELEGRAM_BOT_TOKEN=your_bot_token
```

3. Запустите бота:
```bash
python -m app.telegram_bot
```

## Проверка работоспособности

1. Откройте веб-приложение: http://localhost:3000
2. Найдите бота в Telegram по его username
3. Отправьте команду `/start`
4. Проверьте основные функции:
   - Регистрация пользователя
   - Добавление напитков
   - Просмотр статистики
   - Настройка уведомлений

## Возможные проблемы

1. Ошибка подключения к базе данных:
   - Проверьте, что PostgreSQL запущен
   - Проверьте правильность данных в DATABASE_URL

2. Ошибки фронтенда:
   - Очистите кэш npm: `npm cache clean --force`
   - Удалите node_modules и переустановите зависимости

3. Ошибки бэкенда:
   - Проверьте логи uvicorn
   - Убедитесь, что все зависимости установлены

4. Проблемы с Telegram ботом:
   - Проверьте правильность токена
   - Убедитесь, что бот не заблокирован 