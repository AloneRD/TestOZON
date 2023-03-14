from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.datebase import get_session
from app.models.account import Account


payment_router = APIRouter(
    prefix='/pay',
    tags=['Pay System']
)


@payment_router.get('/balance/account/{id:int}')
async def get_balance(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Account).where(Account.id == id))
    account = result.scalar()
    return JSONResponse({"balance": account.balance})
