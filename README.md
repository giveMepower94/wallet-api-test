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