from FormulaCommit.parse import ParsePythonManager
from FormulaCommit.parse_sql import ParseSqlManager


class AbstractField:
    def __init__(self):
        self._symbol = None
        self._formula = None
        self._value = None
        self._independent_parser_manager = None

    @property
    def dependence(self):
        return set(self._independent_parser_manager.parses(self._formula))

    def prepare_calc(self, *, fields_values_dict=None):
        if type(self._independent_parser_manager) == ParseSqlManager:
            self.__prepare_calc_mysql()
        elif type(self._independent_parser_manager) == ParsePythonManager:
            self.__prepare_calc_python(fields_values_dict=fields_values_dict)

    def __prepare_calc_mysql(self):
        self._value = self._independent_parser_manager.prepare_calc(field_symbol=self._symbol,
                                                                    formula_string=self._formula)

    def __prepare_calc_python(self, *, fields_values_dict):
        self._value = self._independent_parser_manager.prepare_calc(formula_string=self._formula,
                                                                    field_value_dict=fields_values_dict)

    # def prepare_calc(self, fields_values_dict):
    #     self._value = self._independent_parser_manager.prepare_calc(self._formula, fields_values_dict)  # todo не всегда корректный параметр необходимо использовать интерфейс


class IntegerField(AbstractField):

    def __init__(self, *, symbol, formula):
        super().__init__()
        self._symbol = symbol
        self._formula = formula

    def calc(self):
        self._value = float(eval(str(self._value)))  # Расчет, округление
        return self._value


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
