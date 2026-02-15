from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

from app.config import settings
from app.models import Transaction, User

_initialized = False


async def init_db() -> None:
    client = AsyncIOMotorClient(settings.mongodb_url)
    await init_beanie(
        database=client[settings.database_name],
        document_models=[User, Transaction],
    )


async def ensure_db() -> None:
    """Call before any DB access. Inits once; on Vercel this avoids crashing at startup if MongoDB is slow."""
    global _initialized
    if _initialized:
        return
    try:
        await init_db()
        _initialized = True
    except ServerSelectionTimeoutError as e:
        raise RuntimeError(
            "Could not connect to MongoDB. Check MONGODB_URL and network access (e.g. Atlas allowlist)."
        ) from e
