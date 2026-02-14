from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс для всех ORM-моделей SQLAlchemy.
    Хранит общую metadata, которая используется Alembic для миграций."""
    pass
