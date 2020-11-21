import dataclasses

from fastapi import FastAPI
from starlette.responses import Response, JSONResponse

from abilling.api import views
from abilling.app.config import config
from abilling.app.db import Db
from abilling.utils import errors


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

    @app.exception_handler(errors.NotFound)
    async def http_exception_handler(request, exc: errors.NotFound):
        return JSONResponse(exc.dict(), status_code=404)

    @app.exception_handler(404)
    async def http_exception_handler(request, exc):
        return JSONResponse({'error': 'NOT_FOUND'}, status_code=404)

    app.include_router(views.billing_router)

    return app
