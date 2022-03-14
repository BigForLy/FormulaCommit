import graphlib
from abc import abstractmethod, ABC
from FormulaCommit.definition_manager import DefinitionFactory, DefinitionFactoryMysql, DefinitionFactorySqlite
from FormulaCommit.parse_sql import ParserMySQLFactory, ParserSqliteFactory
from FormulaCommit.session_manager import MySQLCalculateFactory, SqliteCalculatorUsingMemoryFactory


#
# @staticmethod
# def __to_fixed_range(number, digit=0):
#     """
#     Округление перед выводом пользователю, позволяет дополнить нулями значение
#     Использует округление в большую сторону, применять для проставления нулей
#     :param number: объект для округления
#     :param digit: количество знаков после запятой
#     :return: значение с определенным количеством знаков после запятой
#     """
#     return f"{number:.{digit}f}"

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


class CalculationMethodForMySql(AbstractCalculationMethod):

    def calc_result(self, symbol_and_calculate_item_list) -> dict:
        parser = ParserMySQLFactory().parser()
        calc_string, select_string = parser.parse(symbol_and_calculate_item_list)
        calculator = MySQLCalculateFactory().calculator()
        dataset_result = calculator.calculation(calc_string, select_string)
        return dataset_result


class CalculationMethodForSqlite(AbstractCalculationMethod):

    def calc_result(self, symbol_and_calculate_item_list) -> dict:
        parser = ParserSqliteFactory().parser()
        calc_string, select_string = parser.parse(symbol_and_calculate_item_list)
        calculator = SqliteCalculatorUsingMemoryFactory().calculator()
        dataset_result = calculator.calculation(calc_string, select_string)
        return dataset_result


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


class CalculationFactoryMySql(AbstractCalculationFactory):

    def calculation_method(self) -> AbstractCalculationMethod:
        return CalculationMethodForMySql()

    def definition_manager(self) -> DefinitionFactory:
        return DefinitionFactoryMysql()


class CalculationFactorySqlite(AbstractCalculationFactory):

    def calculation_method(self) -> AbstractCalculationMethod:
        return CalculationMethodForSqlite()

    def definition_manager(self) -> DefinitionFactory:
        return DefinitionFactorySqlite()


class FormulaCalculation:  # general class

    def __init__(self, data, calculation_manager: AbstractCalculationFactory):
        self.__data = data
        self.__calculation_manager = calculation_manager
        self.__definition_manager = calculation_manager.definition_manager().manager()

    def calc(self):
        """
        Основной метод расчета результата,
        вызывает последовательно методы подготовки параметров для графа,
        расчет графа и вычисление результата
        :return: словарь результатов {ключ1: значение1, ключ2: значение2}
        """
        self._prepare_data_for_calculation()

        graph = self._collects_data_for_graph()

        calculated_graph = self._calculated_graph(graph)

        symbol_and_calculate_item_list = self._collects_the_correct_sequence_of_formulas(calculated_graph)

        calculation_method = self.__calculation_manager.calculation_method()
        dataset_result = calculation_method.calc_result(symbol_and_calculate_item_list)

        return self.__processing_of_calculation_results(dataset_result)

    def _collects_the_correct_sequence_of_formulas(self, calculated_graph):
        symbol_and_calculate_item_list = dict(map(lambda x: (x, self.__definition_manager.get_formula_by_symbol(x)),
                                                  calculated_graph))
        return symbol_and_calculate_item_list

    def _prepare_data_for_calculation(self):
        for current_field in self.__data:
            self.__definition_manager.add(current_field)
        self.__definition_manager.update_data_for_calculating()

    def _collects_data_for_graph(self):
        """
        Подгатавливает параметры для графа
        :return: словарь зависимостей формата dict[str: set]
        """
        return self.__definition_manager.all_field_dependencies_from_formula_symbol

    @staticmethod
    def _calculated_graph(graph):
        """
        Расчет графа по заданным параметрам
        :param graph: словарь зависимостей
        :type graph: dict[str: set]
        :return: кортеж последовательности элементов
        """
        return tuple(graphlib.TopologicalSorter(graph).static_order())

    def __processing_of_calculation_results(self, dataset_result):
        return self.__definition_manager.update_value_for_data(dataset_result)
