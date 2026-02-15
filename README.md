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

## Deploy on Vercel

1. **Root**: If the repo is a monorepo, set **Root Directory** to `backend` so Vercel’s root is this folder (where `app/` and `requirements.txt` live).
2. **Entry**: Vercel looks for FastAPI `app` at `app/index.py`; this repo has `app/index.py` importing `app` from `app.main`.
3. **Environment variables** (all required in Vercel; no defaults in code): In **Project → Settings → Environment Variables** add:
   - `MONGODB_URL` — MongoDB connection string (e.g. Atlas). In Atlas → Network Access, allow **0.0.0.0/0** (or add Vercel’s IPs) so serverless can connect.
   - `DATABASE_NAME` — e.g. `expense_tracker`
   - `JWT_SECRET` — Strong random string for production
   - `JWT_EXPIRE_MINUTES` — e.g. `10080` (7 days)
   - `CORS_ORIGINS` — Comma-separated frontend URLs, e.g. `https://your-app.vercel.app`
4. **Health check**: After deploy, open `https://your-backend-url.vercel.app/`. If you see `{"status":"ok"}`, env vars are loaded and the app started. If you still get 500, open the deployment **Logs** for the real error (often MongoDB connection timeout or missing env var).
5. **Logs**: Deployment → **Logs** shows the traceback (e.g. “Missing required env vars” or MongoDB connection errors).

For full project details and frontend setup, see the [root README](../README.md).
