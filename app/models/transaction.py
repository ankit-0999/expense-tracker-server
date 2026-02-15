from datetime import datetime
from typing import Literal

from beanie import Document, Indexed, PydanticObjectId
from pydantic import BaseModel, Field


class Transaction(Document):
    user_id: Indexed(PydanticObjectId)
    type: Literal["income", "expense"]
    amount: float = Field(gt=0)
    currency: str = "INR"
    category: str
    description: str = ""
    date: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "transactions"


# Request/response schemas
CATEGORIES = [
    "Salary",
    "Food",
    "Rent",
    "Freelance",
    "Transport",
    "Entertainment",
    "Utilities",
    "Shopping",
    "Other",
]


class TransactionCreate(BaseModel):
    type: Literal["income", "expense"]
    amount: float = Field(gt=0)
    currency: str = "INR"
    category: str
    description: str = ""
    date: datetime | None = None


class TransactionUpdate(BaseModel):
    type: Literal["income", "expense"] | None = None
    amount: float | None = Field(None, gt=0)
    currency: str | None = None
    category: str | None = None
    description: str | None = None
    date: datetime | None = None
