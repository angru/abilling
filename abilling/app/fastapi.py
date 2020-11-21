from fastapi import FastAPI

from abilling.api import views
from abilling.app.config import config
from abilling.app.db import Db


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

    app.include_router(views.billing_router)

    return app
