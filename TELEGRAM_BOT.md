# Telegram Bot AlcoControl

## Общая информация

- Название: @AlcoControlBot
- Язык: Python
- Библиотека: python-telegram-bot
- Версия: 20.0+

## Команды

### Основные команды

- `/start` - Начало работы с ботом
- `/help` - Справка по командам
- `/register` - Регистрация нового пользователя
- `/profile` - Просмотр профиля
- `/settings` - Настройки уведомлений

### Команды для работы с напитками

- `/add` - Добавить новый напиток
- `/list` - Список напитков
- `/stats` - Статистика потребления
- `/delete` - Удалить напиток

## Структура бота

```
telegram/
├── __init__.py
├── bot.py              # Основной класс бота
├── handlers/           # Обработчики команд
│   ├── __init__.py
│   ├── start.py
│   ├── register.py
│   ├── drinks.py
│   └── stats.py
├── keyboards/          # Клавиатуры
│   ├── __init__.py
│   ├── main.py
│   └── drinks.py
└── utils/             # Вспомогательные функции
    ├── __init__.py
    ├── validators.py
    └── formatters.py
```

## Примеры кода

### Инициализация бота

```python
from telegram.ext import Application, CommandHandler, MessageHandler, filters

async def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("register", register_command))
    
    # Запуск бота
    await application.run_polling()
```

### Обработчик команды /add

```python
async def add_drink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Проверка регистрации
    if not is_user_registered(user_id):
        await update.message.reply_text(
            "Пожалуйста, сначала зарегистрируйтесь с помощью /register"
        )
        return
    
    # Создание клавиатуры для выбора типа напитка
    keyboard = [
        [InlineKeyboardButton("Пиво", callback_data="beer")],
        [InlineKeyboardButton("Вино", callback_data="wine")],
        [InlineKeyboardButton("Крепкий алкоголь", callback_data="spirits")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Выберите тип напитка:",
        reply_markup=reply_markup
    )
```

## Состояния диалога

### Добавление напитка

1. Выбор типа напитка
2. Ввод названия
3. Ввод объема
4. Ввод крепости
5. Подтверждение

### Регистрация

1. Ввод email
2. Ввод пароля
3. Подтверждение email
4. Создание профиля

## Уведомления

### Типы уведомлений

- Ежедневный лимит
- Предупреждения о превышении
- Напоминания о вводе данных
- Статистика за период

### Пример отправки уведомления

```python
async def send_notification(user_id: int, message: str):
    try:
        await bot.send_message(
            chat_id=user_id,
            text=message,
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logger.error(f"Failed to send notification to {user_id}: {e}")
```

## Обработка ошибок

### Основные исключения

- UserNotRegistered
- InvalidDrinkData
- DatabaseError
- TelegramError

### Пример обработки

```python
try:
    await process_drink_data(update, context)
except UserNotRegistered:
    await update.message.reply_text(
        "Пожалуйста, сначала зарегистрируйтесь"
    )
except InvalidDrinkData:
    await update.message.reply_text(
        "Неверные данные напитка. Попробуйте еще раз"
    )
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    await update.message.reply_text(
        "Произошла ошибка. Попробуйте позже"
    )
```

## Логирование

### Настройка логгера

```python
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
```

### Примеры логирования

```python
logger.info(f"User {user_id} started bot")
logger.warning(f"User {user_id} exceeded daily limit")
logger.error(f"Failed to process drink data: {e}")
```

## Тестирование

### Unit тесты

```python
def test_add_drink():
    update = Mock()
    update.effective_user.id = 123
    context = Mock()
    
    result = add_drink(update, context)
    assert result is not None
    assert "Выберите тип напитка" in result.text
```

### Интеграционные тесты

```python
async def test_full_drink_flow():
    # Имитация добавления напитка
    await add_drink(update, context)
    await handle_drink_type(update, context)
    await handle_drink_name(update, context)
    
    # Проверка результата
    drink = await get_last_drink(123)
    assert drink is not None
    assert drink.type == "beer"
```

## Развертывание

### Требования

- Python 3.9+
- python-telegram-bot
- PostgreSQL
- Redis (для кэширования)

### Конфигурация

```python
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
```

### Запуск

```bash
python -m telegram.bot
```

## Мониторинг

### Метрики

- Количество активных пользователей
- Количество добавленных напитков
- Время отклика команд
- Ошибки и исключения

### Prometheus метрики

```python
from prometheus_client import Counter, Histogram

commands_counter = Counter(
    'bot_commands_total',
    'Total number of bot commands',
    ['command']
)

command_duration = Histogram(
    'bot_command_duration_seconds',
    'Time spent processing command',
    ['command']
)
```

## Безопасность

### Проверки

- Валидация входных данных
- Защита от спама
- Rate limiting
- Проверка прав доступа

### Пример rate limiting

```python
from telegram.ext import MessageHandler, filters
from telegram.error import RetryAfter

async def rate_limit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Проверка лимита
        if await is_rate_limited(update.effective_user.id):
            raise RetryAfter(60)
    except RetryAfter as e:
        await update.message.reply_text(
            f"Пожалуйста, подождите {e.retry_after} секунд"
        )
        return
```

# .env
DATABASE_URL=postgresql://postgres:postgres@localhost/alcocontrol
TELEGRAM_BOT_TOKEN=your_bot_token 