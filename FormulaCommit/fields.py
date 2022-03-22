from abc import ABC, abstractmethod
from dataclasses import dataclass

from FormulaCommit.tools import ConcreteComponentTenToDegree, ConcreteComponentRoundToSignificantDigits, \
    ConcreteComponentRoundWithZero, ConcreteComponentRoundTo


class AbstractField(ABC):

    def __init__(self, *,
                 definition_number,
                 symbol,
                 formula,
                 primary_key,
                 ten_to_degree,
                 round_to,
                 round_to_another_column,
                 round_to_significant_digits,
                 round_with_zeros,
                 validate_calculation,
                 value,
                 **kwargs):
        """

        :param definition_number: номер определения
        :param symbol: символьное обозначение для расчета
        :param formula: формула
        :param primary_key: уникальный ключ для вывода значений, пример: {primary_key1: value1, primary_key2: value2}
        :param ten_to_degree: представление значения a * 10^n
        :param round_to: округление
        :param round_to_another_column: округление относительно другого поля
        :param round_to_significant_digits: округление до значящих цифр
        :param round_with_zeros: дополнение нулями после запятой
        :param validate_calculation: проверка поля с помощью расчета формулы
        :param value: значение
        :param kwargs: словарь не дефолтных параметров
        :attribute _value: значение
        :attribute _value_only: значение приоритетнее формулы
        :attribute _type_value: тип введенного значения
        """
        self._symbol = SymbolItem(symbol, f'{symbol}_{definition_number}') if symbol else None
        self._formula = FormulaItem(formula, set(), f'{symbol}_{definition_number}')
        self._value = None
        self._value_only = False
        self._definition_number = definition_number
        self._primary_key = primary_key
        self._calc_component_before = []
        if round_to:
            self._calc_component_before.append(ConcreteComponentRoundTo)
        self._calc_component = []
        self._round_to = round_to
        if ten_to_degree:
            self._calc_component.append(ConcreteComponentTenToDegree)
        self._round_to = round_to
        self._round_to_another_column = round_to_another_column
        if round_to_significant_digits:
            self._calc_component.append(ConcreteComponentRoundToSignificantDigits)
        if round_with_zeros:
            self._calc_component.append(ConcreteComponentRoundWithZero)
        self._validate_calculation = validate_calculation
        self._value = value
        self._type_value = type(value)
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

    def before_update_component(self):
        for component in self._calc_component_before:
            component().accept(self)

    def after_update_component(self):
        for component in self._calc_component:
            component().accept(self)

    def create_symbol(self, symbol):
        self._symbol = SymbolItem(symbol, f'{symbol}_{self._definition_number}', True)
        self._formula.formula_update_value_component = f'{symbol}_{self._definition_number}'

    def visit_concrete_component_give_value(self, element):
        self._value = element.calc(self._value)

    def visit_concrete_component_give_formula_and_round(self, element):
        self._formula.formula_update_value_component = element.calc(self._formula.formula_update_value_component,
                                                                    self._round_to)

    def visit_concrete_component_give_value_and_round(self, element):
        self._value = element.calc(self._value, self._round_to)


class IntegerField(AbstractField):

    def __init__(self, *,
                 symbol="",
                 formula="",
                 value=None,
                 definition_number=0,
                 primary_key,
                 ten_to_degree=False,
                 round_to=2,
                 round_to_another_column=None,
                 round_to_significant_digits=False,
                 round_with_zeros=False,
                 validate_calculation='',
                 **kwargs):
        super().__init__(definition_number=definition_number,
                         symbol=symbol,
                         formula=formula,
                         primary_key=primary_key,
                         ten_to_degree=ten_to_degree,
                         round_to=round_to,
                         round_to_another_column=round_to_another_column,
                         round_to_significant_digits=round_to_significant_digits,
                         round_with_zeros=round_with_zeros,
                         validate_calculation=validate_calculation,
                         value=value,
                         **kwargs)

    def calc(self):
        self.after_update_component()
        self._value = float(eval(str(self._value))) if self._value else ''  # Расчет, округление


class StringField(AbstractField):

    def __init__(self, *,
                 symbol="",
                 formula="",
                 value=None,
                 definition_number=0,
                 primary_key,
                 ten_to_degree=False,
                 round_to=0,
                 round_to_another_column=None,
                 round_to_significant_digits=False,
                 round_with_zeros=False,
                 validate_calculation='',
                 **kwargs):
        super().__init__(definition_number=definition_number,
                         symbol=symbol,
                         formula=formula,
                         primary_key=primary_key,
                         ten_to_degree=ten_to_degree,
                         round_to=round_to,
                         round_to_another_column=round_to_another_column,
                         round_to_significant_digits=round_to_significant_digits,
                         round_with_zeros=round_with_zeros,
                         validate_calculation=validate_calculation,
                         value=value,
                         **kwargs)
        self._value = value

    def calc(self):
        self.cast_to_original_type_value()
        self.after_update_component()
        self._value = str(self._value) if self._value or self._value == 0 else ''

    def cast_to_original_type_value(self):
        if not self.formula or self._value_only:
            self._value = self._type_value(self._value)


class BoolField(AbstractField):

    def __init__(self, *,
                 symbol="",
                 formula="",
                 value,
                 definition_number=0,
                 primary_key,
                 ten_to_degree=False,
                 round_to=2,
                 round_to_another_column=None,
                 round_to_significant_digits=False,
                 round_with_zeros=False,
                 validate_calculation='',
                 **kwargs):
        super().__init__(definition_number=definition_number,
                         symbol=symbol,
                         formula=formula,
                         primary_key=primary_key,
                         ten_to_degree=ten_to_degree,
                         round_to=round_to,
                         round_to_another_column=round_to_another_column,
                         round_to_significant_digits=round_to_significant_digits,
                         round_with_zeros=round_with_zeros,
                         validate_calculation=validate_calculation,
                         value=value,
                         **kwargs)
        self._value = True if value == 'True' or value == '1' or value == 1 else False

    def calc(self):
        self._value = True if self._value == 'True' or self._value == '1' or self._value == 1 else False


@dataclass
class SymbolItem:
    symbol: str
    symbol_and_definition: str
    overridden: bool = False


@dataclass
class FormulaItem:
    formula: str
    dependence: set
    formula_update_value_component: str
