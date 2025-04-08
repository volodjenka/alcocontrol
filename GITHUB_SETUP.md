# Загрузка проекта на GitHub

## Подготовка проекта

1. Создайте файл `.gitignore`:
```
# Python
__pycache__/
*.py[cod]
*$py.class
venv/
.env

# Node
node_modules/
build/
dist/
.env.local

# IDE
.vscode/
.idea/

# Логи
*.log

# База данных
*.sqlite3
```

2. Инициализируйте Git репозиторий:
```bash
git init
```

3. Добавьте файлы в Git:
```bash
git add .
```

4. Создайте первый коммит:
```bash
git commit -m "Initial commit"
```

## Создание репозитория на GitHub

1. Перейдите на [GitHub](https://github.com)
2. Нажмите "+" в правом верхнем углу
3. Выберите "New repository"
4. Заполните форму:
   - Repository name: `alcocontrol`
   - Description: "Telegram бот для контроля употребления алкоголя"
   - Выберите "Public" или "Private"
   - Не инициализируйте репозиторий с README
5. Нажмите "Create repository"

## Загрузка проекта

1. Свяжите локальный репозиторий с GitHub:
```bash
git remote add origin https://github.com/ваш-username/alcocontrol.git
```

2. Загрузите код:
```bash
git push -u origin main
```

## Настройка GitHub Actions

1. Создайте файл `.github/workflows/ci.yml`:
```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: alcocontrol_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest
    
    - name: Run tests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost/alcocontrol_test
      run: |
        pytest
```

## Защита ветки main

1. Перейдите в настройки репозитория
2. Выберите "Branches"
3. Добавьте правило для ветки `main`:
   - Требовать проверки статуса перед слиянием
   - Требовать проверки кода
   - Запретить прямые пуши в main

## Работа с ветками

1. Создание новой ветки:
```bash
git checkout -b feature/название-функции
```

2. Загрузка изменений:
```bash
git push origin feature/название-функции
```

3. Создание Pull Request:
   - Перейдите на GitHub
   - Нажмите "Compare & pull request"
   - Заполните описание изменений
   - Нажмите "Create pull request"

## Обновление локального репозитория

```bash
git pull origin main
```

## Советы по работе с Git

1. Регулярно делайте коммиты:
```bash
git commit -m "Описание изменений"
```

2. Используйте осмысленные сообщения коммитов
3. Создавайте отдельные ветки для новых функций
4. Регулярно синхронизируйтесь с удаленным репозиторием
5. Проверяйте код перед созданием Pull Request 