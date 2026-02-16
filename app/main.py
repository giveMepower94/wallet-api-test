from fastapi import FastAPI

from app.api.v1.wallets import router as wallets_router

# Создаем экземпляр приложения
app = FastAPI(title="wallet-api-test")

app.include_router(wallets_router)


# Проверяем здоровье нашего проекта
@app.get("/health")
def healthcheck():
    return {"status": "ok"}
