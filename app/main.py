from fastapi import FastAPI
from sqlalchemy import text

from app.database.session import engine

from app.api.v1.endpoints.auth import router as auth_router

from app.api.v1.endpoints import category 

from app.api.v1.endpoints import expense

from app.api.v1.endpoints import dashboard

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

from app.api.v1.endpoints import users
from app.api.v1.endpoints import company

from app.api.v1.endpoints import department
from app.api.v1.endpoints import position
from app.utils.seed_admin import seed_admin
import socket


app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://expense-tracker-ui-olive.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    seed_admin()

app.include_router(auth_router)
app.include_router(category.router)
app.include_router(expense.router)
app.include_router(dashboard.router)
app.include_router(company.router)
app.include_router(position.router)

app.include_router(users.router)
app.include_router(department.router)

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

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


@app.get("/smtp-test")
def smtp_test():
    try:
        socket.create_connection(("smtp.gmail.com", 587), timeout=10)
        return {"status": "Connected to Gmail SMTP"}
    except Exception as e:
        return {
            "status": "Failed",
            "error": str(e)
        }