# Expense Tracker Backend

A FastAPI-based backend application for managing expenses, authentication, analytics, and reporting.

## Features

* User Authentication (JWT)
* Expense CRUD Operations
* Expense Search and Filtering
* Dashboard Analytics
* CSV Export
* PostgreSQL Database
* Docker Support
* REST APIs with Swagger Documentation

## Tech Stack

* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* JWT Authentication
* Docker

## Project Structure

```text
app/
├── api/
├── core/
├── database/
├── models/
├── repositories/
├── schemas/
├── services/
└── main.py
```

## Local Setup

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

## Docker Setup

Build and start containers:

```bash
docker compose up --build
```

Backend will be available at:

```text
http://localhost:8000
```

## API Features

* Authentication
* Expense Management
* Dashboard Analytics
* Expense Search
* Expense Filtering
* CSV Export

## Author

Sujana Nagaraj
