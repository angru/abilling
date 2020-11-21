import enum


class OperationType(str, enum.Enum):
    ACCRUAL = 'ACCRUAL'
    WRITE_OFF = 'WRITE_OFF'