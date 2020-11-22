import typing as t
from decimal import Decimal

from pydantic import BaseModel, validator, root_validator


class NewClient(BaseModel):
    name: str


class Wallet(BaseModel):
    id: int
    balance: str


class Client(NewClient):
    id: int
    wallet: Wallet


class ChargeInfo(BaseModel):
    wallet_id: int
    amount: str

    @validator('amount')
    def check_amount(cls, amount):
        amount = Decimal(amount)

        if amount <= 0:
            raise ValueError('amount must be greater than 0')

        return amount


class TransferInfo(BaseModel):
    wallet_from: int
    wallet_to: int
    amount: str

    @validator('amount')
    def check_amount(cls, amount):
        amount = Decimal(amount)

        if amount <= 0:
            raise ValueError('amount must be greater than 0')

        return amount

    @root_validator(skip_on_failure=True)
    def check_wallets_are_different(cls, data):
        if data['wallet_from'] == data['wallet_to']:
            raise ValueError('Wallets are equal')

        return data


class ErrorInfo(BaseModel):
    error: str
    message: str = None
    detail: t.Any = None
