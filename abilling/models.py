import sqlalchemy as sa
from sqlalchemy.sql import func

from abilling.app.config import config
from abilling.utils.constants import OperationType

metadata = sa.MetaData(schema=config.DB_PG_SCHEMA)

client = sa.Table(
    'client',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column('date', sa.DateTime(timezone=True), nullable=False, server_default=func.now()),
    sa.Column('name', sa.String(255), nullable=False),
)


currency = sa.Table(
    'currency',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column('code', sa.String(255), nullable=False),
    sa.UniqueConstraint('code', name='uc_currency_name'),
    sa.Index('ix_currency_code', 'code', unique=True),
)

wallet = sa.Table(
    'wallet',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column(
        'client_id',
        sa.ForeignKey('client.id', name='fk_wallet_client_id'),
        nullable=False,
    ),
    sa.Column(
        'currency_id',
        sa.ForeignKey('currency.id', name='fk_wallet_currency_id'),
        nullable=False,
    ),
    sa.Column('balance', sa.DECIMAL, nullable=False, server_default=sa.text('0')),
    sa.Index('ix_wallet_client_id', 'client_id'),
    sa.CheckConstraint('balance >= 0', name='check_balance_cant_be_negative'),
)

transaction = sa.Table(
    'transaction',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column('date', sa.DateTime(timezone=True), nullable=False, server_default=func.now()),
    sa.Column(
        'wallet_id',
        sa.ForeignKey('wallet.id', name='fk_transaction_wallet_id'),
        nullable=False,
    ),
    sa.Column(
        'type',
        sa.Enum(OperationType, name='operation_type', schema=config.DB_PG_SCHEMA),
        nullable=False,
    ),
    sa.Column('amount', sa.DECIMAL, nullable=False),
    sa.Column('description', sa.JSON),
    sa.Index('ix_transaction_wallet_id', 'wallet_id'),
)
