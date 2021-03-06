from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from abilling.api import controllers
from abilling.api.serializers import NewClient, Client, ChargeInfo, TransferInfo, ErrorInfo
from abilling.app.db import Db
from abilling.app.dependencies import db

billing_router = APIRouter()

ERROR_RESPONSES = {
    404: {'model': ErrorInfo, 'description': 'Not found'},
    422: {'model': ErrorInfo, 'description': 'Validation error'},
    500: {'model': ErrorInfo, 'description': 'Internal error'},
}


@billing_router.post(
    path='/clients',
    status_code=201,
    response_model=Client,
    description='Создание клиента с кошельком',
    responses=ERROR_RESPONSES,
)
async def create_client(client: NewClient, db_manager: Db = Depends(db)):
    return await controllers.create_client(name=client.name, db=db_manager)


@billing_router.get(
    path='/clients/{client_id}',
    response_model=Client,
    description='Получение информации о клиенте по идентификатору',
    responses=ERROR_RESPONSES,
)
async def get_client(client_id: int, db_manager: Db = Depends(db)):
    return await controllers.get_client(client_id=client_id, db=db_manager)


@billing_router.post(
    path='/charges',
    status_code=204,
    description='Начисление средств на кошелек',
    responses=ERROR_RESPONSES,
)
async def charge(operation_info: ChargeInfo, db_manager: Db = Depends(db)):
    await controllers.charge_wallet(**operation_info.dict(), db=db_manager)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@billing_router.post(
    path='/transfers',
    status_code=204,
    description='Перевод средств с одного кошелька на другой',
    responses=ERROR_RESPONSES,
)
async def transfer(operation_info: TransferInfo, db_manager: Db = Depends(db)):
    await controllers.make_transfer(**operation_info.dict(), db=db_manager)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
