from pydantic import BaseModel


class AccountShema(BaseModel):
    id: int
    name: str
    balance: int
