from pydantic import BaseModel, validator, ValidationError
from typing import Optional, Literal


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
    method: Literal['plus', 'minus']

    @validator('summa')
    def summa_must_positiv_integer(cls, v):
        if v < 0:
            raise ValueError("Сумма пополнения не может быть отризательной")
        return v
