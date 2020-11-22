import enum


class OperationType(str, enum.Enum):
    ACCRUAL = 'ACCRUAL'
    WRITE_OFF = 'WRITE_OFF'


class ErrorType(str, enum.Enum):
    VALIDATION_ERROR = 'VALIDATION_ERROR'
    INTERNAL_ERROR = 'INTERNAL_ERROR'
    NOT_FOUND = 'NOT_FOUND'
    OBJECT_NOT_FOUND = 'OBJECT_NOT_FOUND'
    NOT_ENOUGH_MONEY = 'NOT_ENOUGH_MONEY'
