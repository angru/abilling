class EqMock:
    value = ...

    def __init__(self, store_value=False):
        self.store_value = store_value

    def __repr__(self):
        if self.value:
            return 'Not compared yet'

        return str(self.value)

    def __eq__(self, other):
        if self.store_value:
            if self.value is ...:
                self.value = other
        else:
            self.value = other

        return self.value == other
