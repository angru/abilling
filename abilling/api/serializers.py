import typing as t

from pydantic import BaseModel


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


class TransferInfo(BaseModel):
    wallet_from: int
    wallet_to: int
    amount: str


class ErrorInfo(BaseModel):
    error: str
    message: str = None
    detail: t.Any = None
