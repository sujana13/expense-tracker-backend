from fastapi import FastAPI
from sqlalchemy import text

from app.database.session import engine

from app.api.v1.endpoints.auth import router as auth_router

app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0"
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "message": "Expense Tracker API Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/db-health")
def db_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "database": "connected"
        }

    except Exception as e:
        return {
            "database": "disconnected",
            "error": str(e)
        }