import datetime
import graphlib
from abc import abstractmethod, ABC
from sqlalchemy import text
from FormulaCommit.definition_manager import DefinitionManager
from FormulaCommit.session_manager import MySQLFactory, ParserCalculationItemToExecuteStringMySQL, ParserMySQLFactory


class AbstractFormulaManager(ABC):
    """
    Абстрактный класс менеджера формул

    Methods
    -------
    calc
    """

    def __init__(self):
        self.__data = None
        self._result = {}

    @staticmethod
    def __to_fixed_range(number, digit=0):
        """
        Округление перед выводом пользователю, позволяет дополнить нулями значение
        Использует округление в большую сторону, применять для проставления нулей
        :param number: объект для округления
        :param digit: количество знаков после запятой
        :return: значение с определенным количеством знаков после запятой
        """
        return f"{number:.{digit}f}"

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

        return self._calc_result(calculated_graph)

    @abstractmethod
    def _prepare_data_for_calculation(self):
        pass

    @staticmethod
    def _calculated_graph(graph):
        """
        Расчет графа по заданным параметрам
        :param graph: словарь зависимостей
        :type graph: dict[str: set]
        :return: кортеж последовательности элементов
        """
        return tuple(graphlib.TopologicalSorter(graph).static_order())

    @abstractmethod
    def _collects_data_for_graph(self):
        """
        Подгатавливает параметры для графа
        :return: словарь зависимостей формата dict[str: set]
        """
        pass

    @abstractmethod
    def _calc_result(self, calculated_graph):
        """
        Вычисление результата
        :param calculated_graph: кортеж элементов отсортированный в необходимой последовательности рассчета
        :return:
        """
        pass


class FormulaManagerMySql(AbstractFormulaManager):

    def __init__(self, data):
        super().__init__()
        self.__data = data
        self.__definition_manager = DefinitionManager()

    def _prepare_data_for_calculation(self):
        for current_field in self.__data:
            self.__definition_manager.add(current_field)
        self.__definition_manager.update_data_for_calculating()

    def _collects_data_for_graph(self):
        return self.__definition_manager.all_field_dependencies_from_formula_symbol

    def _calc_result(self, calculated_graph):
        symbol_and_calculate_item_list = self._collects_the_correct_sequence_of_formulas(calculated_graph)
        parser = ParserMySQLFactory().parser()
        calc_string, select_string = parser.parse(symbol_and_calculate_item_list)
        calculator = MySQLFactory().calculator()
        dataset_result = calculator.calculation(calc_string, select_string)
        return self.__processing_of_calculation_results(dataset_result)

    def _collects_the_correct_sequence_of_formulas(self, calculated_graph):
        symbol_and_calculate_item_list = dict(map(lambda x: (x, self.__definition_manager.get_formula_by_symbol(x)),
                                                  calculated_graph))
        return symbol_and_calculate_item_list

    def __processing_of_calculation_results(self, dataset_result):  # временное решение
        return self.__definition_manager.update_value_for_data(dataset_result)
