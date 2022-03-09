from abc import ABC, abstractmethod
from dataclasses import dataclass


class AbstractField(ABC):
    def __init__(self):
        self._symbol = None
        self._formula = None
        self._value = None
        self._value_only = False
        self._definition_number = None
        self._field_number = None  # для иденнтификация поля

    @property
    def dependence(self):
        """
        Getter _dependence, обращаться как к атрибуту
        :return: Множество всех существующих символьных обозначений в формуле
        """
        return self._formula.dependence

    @dependence.setter
    def dependence(self, value):
        """
        Setter _dependence, обращаться как к переменной
        :param value: Множество элементов
        """
        self._formula.dependence = value

    @property
    def definition_number(self):
        return self._definition_number

    @property
    def formula(self):
        """
        Getter _formula, обращаться как к атрибуту
        :return: Строка с формулой
        """
        return self._formula.formula

    @property
    def formula_item(self):
        """
        Getter _formula, обращаться как к атрибуту
        :return: Строка с формулой
        """
        return self._formula

    @formula.setter
    def formula(self, value):
        """
        Setter _formula, обращаться как к переменной
        :param value: Строка с формулой
        """
        self._formula.formula = value

    @property
    def symbol_item(self):
        return self._symbol

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @abstractmethod
    def calc(self):
        pass

    def create_symbol(self, symbol):
        self._symbol = SymbolItem(symbol, f'{symbol}_{self._definition_number}', True)


class IntegerField(AbstractField):

    def __init__(self, *, symbol, formula, value=None, definition_number=0):
        super().__init__()
        if symbol:
            self._symbol = SymbolItem(symbol, f'{symbol}_{definition_number}')
        self._formula = FormulaItem(formula, set())
        self._value = value
        self._definition_number = definition_number

    def calc(self):
        self._value = float(eval(str(self._value))) if self._value else ''  # Расчет, округление
        return self._value


class StringField(AbstractField):

    def __init__(self, *, symbol, formula, value=None, definition_number=1):
        super().__init__()
        self._symbol = SymbolItem(symbol, f'{symbol}_{definition_number}')
        self._formula = FormulaItem(formula, set())
        self._value = value
        self._definition_number = definition_number

    def calc(self):
        return self._value


class BoolField(AbstractField):

    def __init__(self, *, symbol, formula=None, value, definition_number=1):
        super().__init__()
        self._symbol = SymbolItem(symbol, f'{symbol}_{definition_number}')
        self._formula = FormulaItem(formula, set())
        self._value = True if value == 'True' else False
        self._definition_number = definition_number

    def calc(self):
        pass


@dataclass
class SymbolItem:
    symbol: str
    symbol_and_definition: str
    overridden: bool = False


@dataclass
class FormulaItem:
    formula: str
    dependence: set
