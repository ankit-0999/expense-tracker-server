from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, summary, transactions

app = FastAPI(
    title="Expense Tracker API",
    description="Personal Income & Expense Tracker",
)


@app.get("/", tags=["health"])
def root():
    """Health check; no DB required. If this returns 200, env vars are loaded."""
    return {"status": "ok"}

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
