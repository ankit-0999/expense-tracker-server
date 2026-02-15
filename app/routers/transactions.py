from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from beanie import PydanticObjectId

from app.dependencies import get_current_user
from app.models import Transaction, User
from app.models.transaction import (
    CATEGORIES,
    TransactionCreate,
    TransactionUpdate,
)

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/categories")
async def list_categories(user: User = Depends(get_current_user)):
    """Return allowed categories for the transaction form dropdown."""
    return {"categories": CATEGORIES}


@router.get("")
async def list_transactions(
    user: User = Depends(get_current_user),
    month: str | None = Query(None, description="Filter by month YYYY-MM"),
):
    query = Transaction.find(Transaction.user_id == user.id)
    if month:
        try:
            year, month_num = map(int, month.split("-"))
            start = datetime(year, month_num, 1)
            if month_num == 12:
                end = datetime(year + 1, 1, 1)
            else:
                end = datetime(year, month_num + 1, 1)
            query = query.find(
                Transaction.date >= start,
                Transaction.date < end,
            )
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid month format. Use YYYY-MM",
            )
    items = await query.sort(-Transaction.date).to_list()
    return items


@router.post("")
async def create_transaction(
    data: TransactionCreate,
    user: User = Depends(get_current_user),
):
    if data.category not in CATEGORIES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category must be one of: {CATEGORIES}",
        )
    tx = Transaction(
        user_id=user.id,
        type=data.type,
        amount=data.amount,
        currency=data.currency,
        category=data.category,
        description=data.description or "",
        date=data.date or datetime.utcnow(),
    )
    await tx.insert()
    return tx


@router.get("/{id}")
async def get_transaction(
    id: PydanticObjectId,
    user: User = Depends(get_current_user),
):
    tx = await Transaction.get(id)
    if not tx or tx.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )
    return tx


@router.put("/{id}")
async def update_transaction(
    id: PydanticObjectId,
    data: TransactionUpdate,
    user: User = Depends(get_current_user),
):
    tx = await Transaction.get(id)
    if not tx or tx.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )
    update_data = data.model_dump(exclude_unset=True)
    if "category" in update_data and update_data["category"] not in CATEGORIES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category must be one of: {CATEGORIES}",
        )
    update_data["updated_at"] = datetime.utcnow()
    await tx.update({"$set": update_data})
    updated = await Transaction.get(id)
    return updated


@router.delete("/{id}")
async def delete_transaction(
    id: PydanticObjectId,
    user: User = Depends(get_current_user),
):
    tx = await Transaction.get(id)
    if not tx or tx.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )
    await tx.delete()
    return {"message": "Deleted"}