"""add-usd

Revision ID: 698ab874e248
Revises: 12a3530f7109
Create Date: 2020-11-22 23:29:08.516952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from abilling.app.config import config

revision = '698ab874e248'
down_revision = '12a3530f7109'
branch_labels = None
depends_on = None


def upgrade():
    t_currency = sa.Table(
        'currency',
        sa.MetaData(),
        sa.Column('code', sa.String(255), nullable=False),
        schema=config.DB_PG_SCHEMA,
    )

    op.bulk_insert(t_currency, [{'code': 'USD'}])


def downgrade():
    pass
