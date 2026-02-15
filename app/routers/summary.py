from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_current_user
from app.models import Transaction, User

router = APIRouter(tags=["summary"])


@router.get("/summary")
async def get_summary(
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
    all_tx = await query.to_list()
    total_income = sum(t.amount for t in all_tx if t.type == "income")
    total_expense = sum(t.amount for t in all_tx if t.type == "expense")
    balance = total_income - total_expense
    by_category: dict[str, float] = {}
    for t in all_tx:
        key = t.category
        if key not in by_category:
            by_category[key] = 0.0
        if t.type == "income":
            by_category[key] += t.amount
        else:
            by_category[key] -= t.amount
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "category_breakdown": by_category,
    }
