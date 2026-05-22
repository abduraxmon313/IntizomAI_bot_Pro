from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from pydantic import BaseModel

from database.db import AsyncSessionLocal
from bot.services.user_service import get_user_by_telegram_id
from bot.services.plan_service import get_today_plans

router = APIRouter()


class PlanOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    scheduled_time: Optional[str] = None
    plan_date: str
    status: str
    score_value: int
    created_at: str


class UserOut(BaseModel):
    telegram_id: int
    full_name: Optional[str] = None
    username: Optional[str] = None
    streak: int
    total_score: int


class PlansResponse(BaseModel):
    user: UserOut
    plans: list[PlanOut]


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/plans", response_model=PlansResponse)
async def get_user_plans(
    telegram_id: int,
    session: AsyncSession = Depends(get_session),
):
    user = await get_user_by_telegram_id(session, telegram_id)

    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    plans = await get_today_plans(session, user)

    return PlansResponse(
        user=UserOut(
            telegram_id=user.telegram_id,
            full_name=user.full_name or "Foydalanuvchi",
            username=user.username,
            streak=user.streak,
            total_score=user.total_score,
        ),
        plans=[
            PlanOut(
                id=p.id,
                title=p.title,
                description=p.description,
                scheduled_time=p.scheduled_time,
                plan_date=str(p.plan_date),
                status=p.status.value,
                score_value=p.score_value,
                created_at=p.created_at.isoformat(),
            )
            for p in plans
        ],
    )
