import typing as t

from abilling.utils.constants import ErrorType


class BaseError(Exception):
    error: str = ErrorType.INTERNAL_ERROR
    message: str = None
    detail: t.Any = None

    def __init__(
            self,
            error: str = None,
            message: t.Optional[str] = None,
            detail: t.Any = None,
    ):
        self.error = error or self.error
        self.message = message
        self.detail = detail

    def dict(self):
        return {
            'error': self.error,
            'message': self.message,
            'detail': self.detail,
        }


class NotFound(BaseError):
    error: str = ErrorType.OBJECT_NOT_FOUND


class NotEnoughMoney(BaseError):
    error: str = ErrorType.NOT_ENOUGH_MONEY
