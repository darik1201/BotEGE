
# Telegram Bot для записи баллов ЕГЭ

Бот для учета и анализа баллов ЕГЭ с возможностью:
- Регистрации учеников
- Ввода баллов по предметам
- Просмотра статистики
- Хранения истории результатов

## Технологии
- Python 3.12
- Aiogram 3.x (асинхронный Telegram Bot API)
- SQLAlchemy 2.0 (ORM)
- Alembic (миграции БД)
- Docker

## Структура проекта
```
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── requirements.txt
└── src
    ├── crud
    │   ├── crud.py
    │   └── __init__.py
    ├── database
    │   ├── database.py
    │   └── __init__.py
    ├── handlers
    │   ├── common.py
    │   └── __init__.py
    ├── keyboards
    │   ├── __init__.py
    │   └── keyboards.py
    ├── main.py
    ├── migration
    │   ├── __init__.py
    │   └── migration.py
    ├── models
    │   ├── __init__.py
    │   └── models.py
    └── states
        ├── __init__.py
        └── states.py
```
## Установка

1. Клонировать репозиторий:
```bash
git clone https://github.com/yourusername/ege-bot.git
cd ege-bot
```

2. Установить зависимости:
```bash
pip install -r requirements.txt
```

3. Заполните переменные в `.env`:
```env
BOT_TOKEN=your_telegram_bot_token
```

## Настройка БД
1. Для создания новой миграции моделей:
```bash
alembic revision --autogenerate -m "Initial tables"
alembic upgrade head
```

## Запуск
```bash
docker-compose build --no-cache && docker-compose up -d
```

## Команды бота
- `/start` - Начало работы
- `/register` - Регистрация
- `/enter_scores` - Ввод баллов
- `/view_scores` - Просмотр результатов
- `/help` - Помощь

![изображение](https://github.com/user-attachments/assets/22f7125e-f192-4708-adda-d54753a2b6fc)


## Лицензия
MIT
