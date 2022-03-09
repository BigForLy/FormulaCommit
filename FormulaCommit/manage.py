import datetime
import graphlib
from abc import abstractmethod, ABC
from sqlalchemy import text
from FormulaCommit.definition_manager import DefinitionManager


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
    def __to_fixed_range(number, digit=0):  # todo: Переименовать
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

        self._calc_result(calculated_graph)

        return self._result

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

    def __init__(self, data, session):
        super().__init__()
        self.__data = data
        self.__session = session
        self._result = {}
        self.__definition_manager = DefinitionManager()

    def _prepare_data_for_calculation(self):
        for current_field in self.__data:
            self.__definition_manager.add(current_field)
        self.__definition_manager.update_data_for_calculating()

    def _collects_data_for_graph(self):
        return self.__definition_manager.all_field_dependencies_from_formula_symbol

    def _calc_result(self, calculated_graph):
        calc_string, select_string = self._collects_the_correct_sequence_of_formulas(calculated_graph)
        dataset_result: dict = self.__data_processing(session=self.__session, calc_string=calc_string,
                                                      select_string=select_string)
        self.__processing_of_calculation_results(dataset_result)

    def _collects_the_correct_sequence_of_formulas(self, calculated_graph):
        symbol_and_formula = dict(map(lambda x: (x, self.__definition_manager.get_formula_by_symbol(x)),
                                      calculated_graph))
        calc_string = ' '.join(symbol_and_formula.values())
        select_string = ', '.join(symbol_and_formula.keys())
        print(calc_string)
        return calc_string, select_string

    @staticmethod
    def __data_processing(*, session, calc_string, select_string):
        foo = datetime.datetime.now()
        session.execute(text(calc_string))
        dataset = session.execute(text('select ' + select_string)).all()
        bar = datetime.datetime.now()
        print('Запрос к базе:   ', bar-foo)
        return dataset[0]._mapping

    def __processing_of_calculation_results(self, dataset_result):
        for symbol, value in dataset_result.items():
            current_field = self.__definition_manager.get_field_by_symbol(symbol)
            current_field.value = value
            current_field.calc()
            self._result.update({symbol: current_field.value})
