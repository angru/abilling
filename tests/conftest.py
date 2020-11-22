import pytest
import sqlalchemy as sa
from alembic.command import upgrade, downgrade
from alembic.config import Config as AlembicConfig

from abilling import models
from abilling.app.config import config as app_config
from abilling.app.db import Db

ALEMBIC_CONFIG = 'alembic.ini'


@pytest.fixture
async def db():
    db = Db(app_config.DB_PG_URL)

    await db.init()

    yield db

    await db.stop()


class TestWithDb:
    @pytest.fixture(autouse=True, scope='session')
    def db_session(self):
        if app_config.ENVIRONMENT != 'testing':
            raise ValueError(
                'Are you insane? Running tests on environments different from "testing" '
                'is strongly not recommended. '
                f'Environment: {app_config.ENVIRONMENT}',
            )

        config = AlembicConfig(ALEMBIC_CONFIG)
        config.attributes['configure_logger'] = False

        upgrade(config, 'head')

        yield

        downgrade(config, 'base')

    @pytest.fixture(autouse=True)
    def clear_data(self, db_session):
        yield 'I will clear tables for you'

        engine = sa.create_engine(app_config.DB_PG_URL)

        with engine.connect() as conn:
            conn.execute(models.transaction.delete())
            conn.execute(models.wallet.delete())
            conn.execute(models.client.delete())
