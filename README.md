# AlcoControl / SoberTrack

Telegram бот с веб-приложением для отслеживания потребления алкоголя и периодов трезвости.

## Функциональность

- Отслеживание потребления алкоголя
- Учет периодов трезвости
- Статистика и аналитика
- Финансовый учет
- Система целей и достижений
- BAC калькулятор (опционально)

## Технологический стек

### Бэкенд
- Python 3.9+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Python-telegram-bot

### Фронтенд
- React
- TypeScript
- Material-UI
- Chart.js
- Tailwind CSS

## Установка и запуск

1. Клонировать репозиторий
2. Установить зависимости:
```bash
pip install -r requirements.txt
cd frontend && npm install
```

3. Создать файл .env и настроить переменные окружения:
```
TELEGRAM_BOT_TOKEN=your_bot_token
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your_secret_key
```

4. Запустить бэкенд:
```bash
uvicorn app.main:app --reload
```

5. Запустить фронтенд:
```bash
cd frontend && npm run dev
```

## Лицензия

MIT 