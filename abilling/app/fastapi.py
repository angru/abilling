from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from abilling.api import views
from abilling.app.config import config
from abilling.app.db import Db
from abilling.utils import errors
from abilling.utils.constants import ErrorType

STATUS_CODE_BY_ERROR = {
    errors.NotFound: 404,
    errors.NotEnoughMoney: 400,
    errors.BaseError: 500,
}


def apply_error_handlers(app: FastAPI):
    @app.exception_handler(errors.BaseError)
    async def handle_app_error(request, exc: errors.BaseError):
        return JSONResponse(exc.dict(), status_code=STATUS_CODE_BY_ERROR[type(exc)])

    @app.exception_handler(404)
    async def handle_404_error(request, exc):
        return JSONResponse({'error': ErrorType.NOT_FOUND}, status_code=404)

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request, exc: RequestValidationError):
        return JSONResponse(
            {
                'error': ErrorType.VALIDATION_ERROR,
                'detail': exc.errors(),
            },
            status_code=422,
        )


def create_app() -> FastAPI:
    app = FastAPI()
    db = Db(config.DB_PG_URL)

    app.extra['db'] = db

    @app.on_event("startup")
    async def startup():
        await db.init()

    @app.on_event("shutdown")
    async def shutdown():
        await db.stop()

    apply_error_handlers(app)

    app.include_router(views.billing_router)

    return app
