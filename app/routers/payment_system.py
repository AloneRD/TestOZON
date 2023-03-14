from fastapi import APIRouter


payment_router = APIRouter(
    prefix='/pay',
    tags=['Pay System']
)


@payment_router.get('/balance')
def get_balance():
    return 'Ваш баланс будет тут'
