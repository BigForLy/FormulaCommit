class StringField:

    def __init__(self, *, symbol, formula, range=None):
        self._symbol = symbol
        self._type = str
        self._formula = formula
        self._range = range
        self._value = None

    def parses(self):
        ParseManager()


class IntegerField:

    def __init__(self, *, symbol, formula, range=None):
        self._symbol = symbol
        self._type = int
        self._formula = formula
        self._range = range
        self._value = None
