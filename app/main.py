from fastapi import FastAPI

# Создаем экземпляр приложения
app = FastAPI(title="wallet-api-test")


# Проверяем здоровье нашего проекта
@app.get("/health")
def healthcheck():
    return {"status": "ok"}
