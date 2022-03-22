from abc import ABC, abstractmethod

from FormulaCommit.definition.definition_manager import DefinitionFactory


class AbstractCalculationMethod(ABC):
    """
    Абстрактный класс расчетного метода

    Methods
    -------
    calc_result
    """

    @abstractmethod
    def calc_result(self, symbol_and_calculate_item_list) -> dict:
        """
        Вычисление результата, включает парсер параметров и расчет значений
        :param symbol_and_calculate_item_list:
        :return:
        """
        pass


class AbstractCalculationFactory(ABC):
    """
    Фабрика расчетного менеджера

    Methods
    -------
    calculation_method
    definition_manager
    """

    @abstractmethod
    def calculation_method(self) -> AbstractCalculationMethod:
        """

        :return: экземпляр класса расчетного метода AbstractCalculationMethod
        """
        pass

    @abstractmethod
    def definition_manager(self) -> DefinitionFactory:
        """

        :return: экземпляр класса менеджера определений AbstractDefinition
        """
        pass
