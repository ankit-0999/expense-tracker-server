# Expense Tracker — Backend

FastAPI REST API for the Personal Expense & Income Tracker. Handles authentication (JWT), transaction CRUD, and monthly summary. Uses MongoDB with Beanie ODM.

## Requirements

- **Python 3.10+**
- **MongoDB** (local or [MongoDB Atlas](https://www.mongodb.com/cloud/atlas))

## Setup

```bash
# From project root: expense-tracker/backend
cd backend

# Virtual environment (recommended)
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# macOS / Linux
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Environment

All configuration is loaded from `.env`; nothing is hardcoded. Copy `.env.example` to `.env` and set every value (no static defaults in code).

| Variable | Required | Description |
|----------|----------|-------------|
| `MONGODB_URL` | Yes | MongoDB connection string |
| `DATABASE_NAME` | Yes | Database name |
| `JWT_SECRET` | Yes | Secret for signing JWTs (use a strong value in production) |
| `JWT_ALGORITHM` | No | JWT algorithm (empty = HS256) |
| `JWT_EXPIRE_MINUTES` | Yes | Token expiry in minutes (e.g. 10080 for 7 days) |
| `CORS_ORIGINS` | Yes | Comma-separated allowed origins (e.g. frontend URL) |

## Run

```bash
# Development (reload on file change)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **API:** http://localhost:8000  
- **Interactive docs:** http://localhost:8000/docs  

## API Overview

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | No | Register `{ email, password, name? }` |
| POST | `/auth/login` | No | Login `{ email, password }` → JWT |
| GET | `/transactions` | Bearer | List transactions, optional `?month=YYYY-MM` |
| POST | `/transactions` | Bearer | Create transaction |
| GET | `/transactions/{id}` | Bearer | Get one transaction |
| PUT | `/transactions/{id}` | Bearer | Update transaction |
| DELETE | `/transactions/{id}` | Bearer | Delete transaction |
| GET | `/transactions/categories` | Bearer | List allowed categories |
| GET | `/summary` | Bearer | Summary stats, optional `?month=YYYY-MM` |

Protected routes require header: `Authorization: Bearer <token>`.

## Structure

```
backend/
├── app/
│   ├── main.py          # FastAPI app, CORS, lifespan
│   ├── config.py       # Settings from env
│   ├── database.py     # Beanie + Motor init
│   ├── auth.py         # Password hashing (bcrypt), JWT (jose)
│   ├── dependencies.py # get_current_user
│   ├── models/
│   │   ├── user.py     # User, UserCreate, UserLogin
│   │   └── transaction.py  # Transaction, CATEGORIES, TransactionCreate/Update
│   └── routers/
│       ├── auth.py
│       ├── transactions.py
│       └── summary.py
├── requirements.txt
├── .env.example
└── README.md
```

## Stack

- **FastAPI** — API framework  
- **Beanie** — MongoDB ODM (async)  
- **Pydantic** — Models & validation  
- **python-jose** — JWT  
- **bcrypt** — Password hashing  
- **uvicorn** — ASGI server  

For full project details and frontend setup, see the [root README](../README.md).
