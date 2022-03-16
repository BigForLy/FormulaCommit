from abc import ABC, abstractmethod


# TFr_dinamic.FormatValue

class Component(ABC):

    @abstractmethod
    def accept(self, visitor) -> None:
        """
        Обратите внимание, мы вызываем visitConcreteComponentA, что
        соответствует названию текущего класса. Таким образом мы позволяем
        посетителю узнать, с каким классом компонента он работает.
        """

        pass

    @abstractmethod
    def calc(self, value) -> None:
        pass


class ConcreteComponentTenToDegree(Component):
    """
    представление значения a * 10^n
    """

    def accept(self, visitor) -> None:
        visitor.visit_concrete_component_give_value(self)

    def calc(self, value) -> str:
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

    def calc(self, value) -> float | str:
        if isinstance(value, float):
            return float(value)
        return value


class ConcreteComponentRoundWithZero(Component):
    """
    дополнение нулями после запятой
    """

    def accept(self, visitor) -> None:
        visitor.visit_concrete_component_give_value_and_round(self)

    def calc(self, value, digit=0) -> str:
        if isinstance(value, float):
            return f"{value:.{digit}f}"
        return value
