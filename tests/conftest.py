import uuid
import pytest_asyncio

from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from app.core.db import AsyncSessionLocal, engine
from app.main import app


@pytest_asyncio.fixture(autouse=True)
async def clean_wallets_table():
    # 1) Очистка через "сырой" SQL на уровне engine — меньше шансов поймать busy connection
    async with engine.begin() as conn:
        await conn.exec_driver_sql("TRUNCATE TABLE wallets")
    yield
    # 2) На всякий случай закрываем все соединения пула после теста
    await engine.dispose()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    # lifespan="on" — чтобы FastAPI корректно отрабатывал startup/shutdown
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def wallet_id() -> uuid.UUID:
    w_id = uuid.uuid4()
    async with AsyncSessionLocal() as session:
        await session.execute(
            text("INSERT INTO wallets (id, balance) VALUES (:id, :balance)"),
            {"id": str(w_id), "balance": 0},
        )
        await session.commit()
    return w_id
