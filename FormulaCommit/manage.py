import graphlib

from FormulaCommit.calculation import AbstractCalculationFactory


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

        calculated_graph = self.__definition_manager.calculation_graph_for_data(self.__data)  # todo некорректно вынесено

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
