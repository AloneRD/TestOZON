from sqlalchemy import Column, BigInteger, String

from app.models.__meta__ import Base


class Account(Base):
    """
    Акаунт пользователя
    """
    __tablename__ = 'account'

    id = Column(BigInteger, primary_key=True, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False)
    balance = Column(BigInteger, default=0)