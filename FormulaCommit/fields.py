from FormulaCommit.parse import ParseManager


class AbstractField:
    def __init__(self):
        self._formula = None
        self._value = None
        self._dependence = None  # set()  todo: не используется

    @property
    def dependence(self):
        self._dependence = set(ParseManager().parses(self._formula))
        return self._dependence


class IntegerField(AbstractField):

    def __init__(self, *, symbol, formula, range=0):
        super().__init__()
        self._symbol = symbol
        # self._type = int
        self._formula = formula
        # self._range = range

    def calc(self, field_value_dict):
        self._value = ParseManager().calc_sql(self._formula, field_value_dict)
        return self._value


class StringField(AbstractField):

    def __init__(self, *, symbol, formula, range=None):
        super().__init__()
        self._symbol = symbol
        self._type = str
        self._formula = formula
        # self._range = range
        # self._value = None

    # def parses(self):
    #     pass


class FloatField(AbstractField):

    def __init__(self, *, symbol, formula, range=2):
        super().__init__()
        self._symbol = symbol
        self._type = float
        self._formula = formula
        # self._range = range
        # self._value = None

    # def _parses(self):
    #     self._parses()
