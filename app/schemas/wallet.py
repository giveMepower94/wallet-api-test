from enum import Enum
from pydantic import BaseModel, Field, PositiveInt


# Схема типа операций
class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class WalletOperationIn(BaseModel):
    operation_type: OperationType
    amount: PositiveInt = Field(..., description="Положительный баланс")


class WalletOut(BaseModel):
    wallet_uuid: str
    balance: int
