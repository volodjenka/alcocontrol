# База данных AlcoControl

## Общая информация

- PostgreSQL 14+
- Кодировка: UTF-8
- Коллация: en_US.UTF-8

## Схема базы данных

### Таблица users

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    telegram_id VARCHAR(50) UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_telegram_id ON users(telegram_id);
```

### Таблица drinks

```sql
CREATE TABLE drinks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    volume DECIMAL(10,2) NOT NULL,
    alcohol_content DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_drinks_user_id ON drinks(user_id);
CREATE INDEX idx_drinks_created_at ON drinks(created_at);
```

### Таблица drink_types

```sql
CREATE TABLE drink_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Таблица user_settings

```sql
CREATE TABLE user_settings (
    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    daily_limit DECIMAL(10,2),
    notification_enabled BOOLEAN DEFAULT true,
    notification_time TIME,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## Миграции

Миграции управляются с помощью Alembic. Файлы миграций находятся в директории `alembic/versions/`.

### Создание новой миграции

```bash
alembic revision -m "описание_изменений"
```

### Применение миграций

```bash
alembic upgrade head
```

### Откат миграций

```bash
alembic downgrade -1
```

## Индексы

### Основные индексы

- `users`: email, telegram_id
- `drinks`: user_id, created_at
- `drink_types`: name

### Составные индексы

```sql
CREATE INDEX idx_drinks_user_date ON drinks(user_id, created_at);
```

## Ограничения

### Внешние ключи

- `drinks.user_id` -> `users.id`
- `user_settings.user_id` -> `users.id`

### Уникальные ограничения

- `users.username`
- `users.email`
- `users.telegram_id`
- `drink_types.name`

### Проверки

```sql
ALTER TABLE drinks
    ADD CONSTRAINT check_volume_positive 
    CHECK (volume > 0);

ALTER TABLE drinks
    ADD CONSTRAINT check_alcohol_content 
    CHECK (alcohol_content >= 0 AND alcohol_content <= 100);
```

## Бэкапы

### Автоматическое резервное копирование

```bash
pg_dump -U postgres -d alcocontrol -F c -f backup.dump
```

### Восстановление из бэкапа

```bash
pg_restore -U postgres -d alcocontrol backup.dump
```

## Мониторинг

### Основные метрики

- Количество активных пользователей
- Количество записей о напитках
- Размер базы данных
- Время отклика запросов

### Запросы для мониторинга

```sql
-- Активные пользователи за последние 30 дней
SELECT COUNT(DISTINCT user_id) 
FROM drinks 
WHERE created_at >= NOW() - INTERVAL '30 days';

-- Размер таблиц
SELECT 
    relname as table_name,
    pg_size_pretty(pg_total_relation_size(relid)) as total_size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
```

## Оптимизация

### Настройки PostgreSQL

```ini
# Память
shared_buffers = 1GB
work_mem = 16MB
maintenance_work_mem = 256MB

# Планировщик
random_page_cost = 1.1
effective_cache_size = 3GB

# Журналирование
wal_level = replica
max_wal_senders = 3
```

### Вакуумизация

```sql
VACUUM ANALYZE users;
VACUUM ANALYZE drinks;
```

## Безопасность

### Роли и права

```sql
-- Создание роли для приложения
CREATE ROLE alcocontrol_app WITH LOGIN PASSWORD 'strong_password';

-- Предоставление прав
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO alcocontrol_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO alcocontrol_app;
```

### Шифрование

- Пароли хешируются с использованием bcrypt
- Чувствительные данные в логах маскируются
- Соединение с базой данных через SSL

## Масштабирование

### Репликация

- Настройка master-slave репликации
- Автоматическое переключение при сбое
- Мониторинг задержки репликации

### Партиционирование

```sql
-- Партиционирование таблицы drinks по дате
CREATE TABLE drinks (
    -- существующие колонки
) PARTITION BY RANGE (created_at);

-- Создание партиций
CREATE TABLE drinks_y2024m01 PARTITION OF drinks
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
``` 