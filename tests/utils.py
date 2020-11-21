class EqMock:
    value = ...

    def __init__(self, store_value=False, type=object):
        self.store_value = store_value
        self.type = type

    def __repr__(self):
        if self.value:
            return 'Not compared yet'

        return str(self.value)

    def __eq__(self, other):
        if self.store_value:
            if self.value is ...:
                self.value = other

            return self.value == other and isinstance(other, self.type)

        return isinstance(other, self.type)
