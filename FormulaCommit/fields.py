from abc import ABC, abstractmethod
from dataclasses import dataclass


class AbstractField(ABC):
    def __init__(self, *, definition_number, symbol, formula, primary_key, **kwargs):
        self._symbol = SymbolItem(symbol, f'{symbol}_{definition_number}') if symbol else None
        self._formula = FormulaItem(formula, set())
        self._value = None
        self._value_only = False
        self._definition_number = definition_number
        self._field_number = None  # для иденнтификация поля
        self._primary_key = primary_key
        for name_attr, value_attr in kwargs.items():
            self.__setattr__(name_attr, value_attr)

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

    def __init__(self, *, symbol="", formula="", value=None, definition_number=1, primary_key,  **kwargs):
        super().__init__(definition_number=definition_number, symbol=symbol, formula=formula, primary_key=primary_key, **kwargs)
        self._value = value

    def calc(self):
        self._value = float(eval(str(self._value))) if self._value else ''  # Расчет, округление
        return self._value


class StringField(AbstractField):

    def __init__(self, *, symbol="", formula="", value=None, definition_number=1, primary_key, **kwargs):
        super().__init__(definition_number=definition_number, symbol=symbol, formula=formula, primary_key=primary_key, **kwargs)
        self._value = value

    def calc(self):
        return self._value


class BoolField(AbstractField):

    def __init__(self, *, symbol="", formula="", value, definition_number=1, primary_key, **kwargs):
        super().__init__(definition_number=definition_number, symbol=symbol, formula=formula, primary_key=primary_key, **kwargs)
        self._value = True if value == 'True' else False

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
