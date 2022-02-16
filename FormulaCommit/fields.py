from FormulaCommit.parse import ParsePythonManager
from FormulaCommit.parse_sql import ParseSqlManager


class AbstractField:
    def __init__(self):
        self._formula = None
        self._value = None
        self._dependence = None  # set()  todo: не используется
        self._independent_parser_manager = None

    @property
    def dependence(self):
        # # self._dependence = set(ParseManager().parses(self._formula))
        # self._dependence = set(ParseSqlManager().parses(self._formula))
        self._dependence = set(self._independent_parser_manager.parses(self._formula))
        return self._dependence

    def calc(self, fields_values_dict):
        self._value = self._independent_parser_manager.calc(self._formula, fields_values_dict)  # todo не всегда корректный параметр необходимо использовать интерфейс
        return self._value


class IntegerField(AbstractField):

    def __init__(self, *, symbol, formula):
        super().__init__()
        self._symbol = symbol
        self._formula = formula

    # def calc2(self, field_value_dict):
    #     # self._value = ParseManager().calc(self._formula, field_value_dict)
    #     self._value = ParseSqlManager().calc(self._formula, field_value_dict)
    #     return self._value


class StringField(AbstractField):

    def __init__(self, *, symbol, formula):
        super().__init__()
        self._symbol = symbol
        self._type = str
        self._formula = formula


class FloatField(AbstractField):

    def __init__(self, *, symbol, formula):
        super().__init__()
        self._symbol = symbol
        self._type = float
        self._formula = formula
