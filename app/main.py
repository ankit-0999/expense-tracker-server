from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo.errors import ServerSelectionTimeoutError

from app.config import settings
from app.database import init_db
from app.routers import auth, summary, transactions


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
    except ServerSelectionTimeoutError as e:
        raise RuntimeError(
            "Could not connect to MongoDB. Set MONGODB_URL in .env to a valid connection string."
        ) from e
    yield


app = FastAPI(
    title="Expense Tracker API",
    description="Personal Income & Expense Tracker",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(summary.router)
