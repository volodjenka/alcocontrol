# Руководство по разработке AlcoControl

## Структура проекта

```
alcocontrol/
├── app/                    # Бэкенд приложение
│   ├── api/               # API endpoints
│   ├── core/              # Основные настройки
│   ├── db/                # Модели и схемы базы данных
│   ├── services/          # Бизнес-логика
│   └── telegram/          # Telegram бот
├── frontend/              # Фронтенд приложение
│   ├── public/           # Статические файлы
│   └── src/              # Исходный код
│       ├── components/   # React компоненты
│       ├── hooks/        # React хуки
│       ├── services/     # API сервисы
│       └── utils/        # Вспомогательные функции
├── tests/                # Тесты
├── alembic/              # Миграции базы данных
└── docker/               # Docker конфигурации
```

## Стандарты кодирования

### Python (Бэкенд)

- PEP 8 для стиля кода
- Типизация с использованием type hints
- Docstrings в формате Google
- Максимальная длина строки: 88 символов
- Использование black для форматирования
- Использование isort для сортировки импортов
- Использование flake8 для линтинга

Пример:
```python
from typing import List, Optional

def get_user_drinks(user_id: int, limit: Optional[int] = None) -> List[Drink]:
    """
    Получить список напитков пользователя.

    Args:
        user_id: ID пользователя
        limit: Максимальное количество записей

    Returns:
        List[Drink]: Список напитков
    """
    query = db.query(Drink).filter(Drink.user_id == user_id)
    if limit:
        query = query.limit(limit)
    return query.all()
```

### TypeScript/React (Фронтенд)

- ESLint с конфигурацией Airbnb
- Prettier для форматирования
- Функциональные компоненты с хуками
- Типизация всех пропсов и состояний
- Компоненты в PascalCase
- Файлы компонентов в PascalCase.tsx
- Максимальная длина строки: 100 символов

Пример:
```typescript
interface DrinkFormProps {
  onSubmit: (drink: Drink) => void;
  initialValues?: Partial<Drink>;
}

const DrinkForm: React.FC<DrinkFormProps> = ({ onSubmit, initialValues }) => {
  const [formData, setFormData] = useState<Partial<Drink>>(initialValues || {});

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData as Drink);
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
    </form>
  );
};
```

## Git workflow

1. Создание ветки:
```bash
git checkout -b feature/название-функции
```

2. Коммиты:
- Используйте conventional commits
- Каждый коммит должен быть атомарным
- Пишите осмысленные сообщения коммитов

Примеры:
```
feat: add drink form component
fix: resolve database connection issues
docs: update deployment instructions
```

3. Pull Request:
- Создайте PR в GitHub
- Добавьте описание изменений
- Укажите связанные issues
- Запросите ревью у коллег

## Тестирование

### Бэкенд

1. Unit тесты:
```bash
pytest tests/unit/
```

2. API тесты:
```bash
pytest tests/api/
```

3. Интеграционные тесты:
```bash
pytest tests/integration/
```

### Фронтенд

1. Unit тесты:
```bash
npm test
```

2. E2E тесты:
```bash
npm run test:e2e
```

## Документация

1. API документация:
- Используйте OpenAPI/Swagger
- Документируйте все endpoints
- Добавляйте примеры запросов/ответов

2. Компоненты:
- Документируйте пропсы
- Добавляйте примеры использования
- Описывайте поведение компонента

## CI/CD

1. GitHub Actions:
- Линтинг
- Тестирование
- Сборка
- Деплой

2. Проверки перед мержем:
- Все тесты должны проходить
- Линтер должен быть доволен
- Должно быть минимум 1 одобрение

## Мониторинг и логирование

1. Бэкенд:
- Используйте structured logging
- Добавляйте контекст к логам
- Настройте алерты

2. Фронтенд:
- Отслеживайте ошибки
- Мониторьте производительность
- Собирайте аналитику

## Безопасность

1. Бэкенд:
- Валидация входных данных
- Защита от SQL-инъекций
- Rate limiting
- CORS настройки

2. Фронтенд:
- XSS защита
- CSRF токены
- Безопасное хранение токенов

## Оптимизация

1. Бэкенд:
- Кэширование
- Оптимизация запросов
- Пагинация

2. Фронтенд:
- Code splitting
- Lazy loading
- Оптимизация бандла

## Релизы

1. Версионирование:
- Semantic Versioning
- CHANGELOG.md
- Git tags

2. Процесс:
- Создание release branch
- Тестирование
- Деплой
- Создание тега 