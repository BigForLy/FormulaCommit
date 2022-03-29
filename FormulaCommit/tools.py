from abc import ABC, abstractmethod


# TFr_dinamic.FormatValue

def is_integer(value):  # todo rename
    try:
        if float(value) == float(int(float(value))):
            return int(float(value))
        else:
            return float(value)
    except ValueError:
        return value


class Component(ABC):

    @abstractmethod
    def accept(self, visitor) -> None:
        """
        Обратите внимание, мы вызываем visitConcreteComponentA, что
        соответствует названию текущего класса. Таким образом мы позволяем
        посетителю узнать, с каким классом компонента он работает.
        """

        pass


class ConcreteComponentTenToDegree(Component):
    """
    представление значения a * 10^n
    """

    def accept(self, visitor) -> None:
        visitor.visit_concrete_component_give_value(self)

    @staticmethod
    def calc(value) -> str:
        if isinstance(value, float | int):
            exponential = "{:e}".format(value)
            exponential_list = exponential.split('e')
            return f'{float(exponential_list[0])}*10^{int(exponential_list[1])}'
        return value


class ConcreteComponentRoundToSignificantDigits(Component):
    """
    округление до значящих цифр
    """

    def accept(self, visitor) -> None:
        visitor.visit_concrete_component_give_value(self)

    @staticmethod
    def calc(value) -> float | str:
        if isinstance(value, float):
            return float(value)
        return value


class ConcreteComponentRoundTo(Component):
    """
    округление
    """

    def accept(self, visitor) -> None:
        visitor.visit_concrete_component_give_formula_and_round(self)

    @staticmethod
    def calc(formula, digits=0) -> str:
        return f'(round({formula}, {abs(digits)}))'


class ConcreteComponentRoundWithZero(Component):
    """
    дополнение нулями после запятой
    """

    def accept(self, visitor) -> None:
        visitor.visit_concrete_component_give_value_and_round(self)

    @staticmethod
    def calc(value, digit=0) -> str:
        if isinstance(value, float):
            return f"{value:.{abs(digit)}f}"
        return value


class ConcreteComponentRoundingToInteger(Component):
    """
    округление до целого
    """

    def accept(self, visitor) -> None:
        if not visitor._round_with_zeros:
            visitor.visit_concrete_component_give_value(self)

    @staticmethod
    def calc(value):
        return is_integer(value)
