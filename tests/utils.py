import typing as t


class EqMock:
    """Утилита для тестирования, позволятет проверять значения,
    которые не известны на момент написания теста и не нам не важно, чему они равны,
    главное проверить тип. Привер: идентификаторы, даты
    """

    value = ...

    def __init__(self, type: t.Union[t.Any, t.List[t.Any]] = object, remember: bool = False):
        """
        :param type: Check type of compared value
        :param remember: Remember first checked value and use it to compare next times
        """
        self.type = type
        self.remember = remember

    def __repr__(self):
        if self.value is ...:
            return 'Not compared yet'

        return str(self.value)

    def __eq__(self, other):
        if not isinstance(other, self.type):
            return False

        if self.remember:
            if self.value is ...:
                self.value = other
        else:
            self.value = other

        return self.value == other
