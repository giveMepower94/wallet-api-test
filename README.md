# wallet-api-test
Асинхронный REST API для управления балансом кошельков.

## Стек
- Python 3.11  
- FastAPI  
- PostgreSQL  
- SQLAlchemy (async)  
- Alembic  
- Docker / Docker Compose  
- Pytest  

## Реализовано
- Получение баланса кошелька  
- Пополнение (deposit)  
- Списание (withdraw)  
- Атомарные операции на уровне БД  
- Миграции БД (Alembic)  
- Интеграционные тесты API

## Запуск проекта

```bash
docker-compose up -d --build
```

## Документация API (Swagger)
http://localhost:8000/docs

## Запуск тестов
```bash
docker-compose run --rm app pytest
```

## Примечание
- Операции списания и пополнения реализованы атомарно на уровне БД
- Защита от ухода баланса в минус обеспечивается на уровне SQL-запроса