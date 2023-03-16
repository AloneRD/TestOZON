from pydantic import BaseModel, validator
from typing import Literal


class AccountShema(BaseModel):
    id: int
    name: str
    balance: int

    @validator('balance')
    def summa_must_positiv_integer(cls, v):
        if v < 0:
            raise ValueError("Баланс не может быть отризательным")
        return v

    class Config:
        orm_mode = True


class BalanceShema(BaseModel):
    user_id: int
    summa: int

    @validator('summa')
    def summa_must_positiv_integer(cls, v):
        if v < 0:
            raise ValueError("Сумма пополнения не может быть отризательной")
        return v


class BalanceShemaPlusMinus(BalanceShema):
    method: Literal['plus', 'minus']


class BalanceShemaTransfer(BalanceShema):
    user_id_to: int
