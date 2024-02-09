# Money_control_fastapi_backend

![GitHub](https://img.shields.io/github/license/vital-yano/money_control_fastapi_backend) ![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/kaccuteput/money_control_fastapi_backend)

### Описание
Репозиторий содержить бэкенд с использованием фреймворка FastAPI для приложения по контролю своих расходов. Управление осуществляется с помощью телеграмм бота (буден написан позднее).
Используемый стек:
- Python 3.11
- Fastapi + uvicorn + httpx
- Pytest
- Pyright
- Ruff
- Sqlalchemy + alembic
- Redis
- Postgres
- Docker

Postgres и Redis поднимаются в Docker.

### Инструкция по запуску проекта и работе с ним

Установка виртуального окружения и зависимостей:
```bash
python -m venv venv && source venv/bin/activate && pip install -r req.txt
```

Запуск локальных и тестовых бд и redis:
```bash
make db_and_redis_local
```

Создание таблиц в бд:
```bash
alembic upgrade heads
TESTING=1 alembic upgrade heads
```

Создание индексов в Redis:
```bash
python create_redis_indices.py
```

Запуск тестов: 
```bash
pytest src/tests -svv
```

Запуск приложения:
```bash
python main.py
```

Документация по хэндлерам расположена по адресу:
```
0.0.0.0:8000/docs
```

Для получения кода для регистрации используется сервис SMS.RU (с помощью звонка).
После регистрации добавьте свой SMS_API_ID в файл .env.

### Планы на будущее
На данный момент реализована только регистрация пользователей. Планируется реализовать позже:

- Статьи доходов/расходов
- Кошелёк
- Переводы
- Долги
- Бюджет
