from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.datebase import get_session
from app.models.account import Account
from app.schemas.account import BalanceShemaPlusMinus, AccountShema, BalanceShemaTransfer


payment_router = APIRouter(
    prefix='/pay',
    tags=['Pay System']
)


@payment_router.get('/balance/account/{id:int}')
async def get_balance(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Account).where(Account.id == id))
    account = result.scalar()
    return JSONResponse({"balance": account.balance})


@payment_router.post('/balance/account/change', response_model=AccountShema)
async def top_up_balance(requisites: BalanceShemaPlusMinus, session: AsyncSession = Depends(get_session)):
    user_id = requisites.user_id
    summa = requisites.summa
    method = requisites.method
    if method == 'plus':
        update_data = {'balance': Account.balance + summa}
    else:
        update_data = {'balance': Account.balance - summa}
    result = await session.execute(
        update(Account).where(Account.id == user_id).values(update_data).returning(Account)
    )

    account = result.first()
    valid_date = AccountShema.from_orm(account[0])

    if account is None:
        raise HTTPException(status_code=400, detail=f'Пользователь с id {user_id} не найден')

    await session.commit()
    return valid_date


@payment_router.post('/balance/account/transfer')
async def transfer_money(requisites: BalanceShemaTransfer, session: AsyncSession = Depends(get_session)):
    user_id = requisites.user_id
    summa = requisites.summa
    user_id_to = requisites.user_id_to

    result = await session.execute(select(Account).where(Account.id == user_id))
    user_from = result.scalar()
    if user_from.balance - summa < 0:
        raise HTTPException(status_code=400, detail='Недостаточно средств')
    await session.execute(
        update(Account).where(Account.id == user_id).values({'balance': Account.balance - summa})
    )
    await session.execute(
        update(Account).where(Account.id == user_id_to).values({'balance': Account.balance + summa})
    )
    await session.commit()
    return JSONResponse({'status': 'success'})
