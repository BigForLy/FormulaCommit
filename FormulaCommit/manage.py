import graphlib
from abc import abstractmethod, ABC

from sqlalchemy import text
from FormulaCommit.parse import ParsePythonManager
from FormulaCommit.parse_sql_v2 import ParseSqlManager


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
        graph = self._collects_data_for_graph()

        calculated_graph = self._calculated_graph(graph)

        self._calc_result(calculated_graph)

        return self._result

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

    def __init__(self, data, session, assay_count=1):
        super().__init__()
        self.__data = data
        self.__session = session
        self._result = {}
        self.__parser_manager = ParseSqlManager(assay_count)

    def __update_number_field_by_symbol(self):
        data = {}
        for _, current_field in self.__data.items():
            if current_field._symbol in data:
                data[current_field._symbol] += current_field._opred_number
            else:
                data.update({current_field._symbol: [current_field._opred_number]})
        self.__parser_manager.number_field_by_symbol = data

    def _collects_data_for_graph(self):  # todo разделить на несколько
        self.__update_number_field_by_symbol()
        graph = {}
        for key, current_field in self.__data.items():
            current_field.formula = self.__parser_manager.update_formula(current_field)
            current_field.dependence = self.__parser_manager.update_dependence(current_field)
            graph.update({key: current_field.dependence})
        return graph

    def _calc_result(self, calculated_graph):
        calc_string = self.__preparation_of_data_for_calculation(calculated_graph)
        dataset_result: dict = self.__data_processing(session=self.__session, calc_string=calc_string)
        self.__processing_of_calculation_results(dataset_result)

    def __preparation_of_data_for_calculation(self, calculated_graph):
        calc_formula_list = []
        for field_symbol in calculated_graph:
            current_field = self.__data[field_symbol]
            calc_formula_list.append(
                self.__parser_manager.parameter_for_calculating_the_result(current_field=current_field)
            )
        calc_string = ' '.join(calc_formula_list)
        print(calc_string)
        return calc_string

    def __data_processing(self, session, calc_string):
        session.execute(text(calc_string))
        dataset = session.execute(text('select ' + ', '.join(self.__data.keys()))).all()
        return dataset[0]._mapping

    def __processing_of_calculation_results(self, dataset_result):
        for key, field_class in self.__data.items():
            field_class._value = dataset_result.get(key)
            field_class.calc()
            self._result.update({key: field_class._value})


class FormulaManagerPython(AbstractFormulaManager):

    def __init__(self, data):
        super().__init__()
        self.__data = data
        self._result = {}
        self.__parser_manager = ParsePythonManager()

    def _collects_data_for_graph(self):
        graph = {}
        for key, current_field in self.__data.items():
            dependence = self.__parser_manager.dependence(current_field)
            graph.update({key: dependence})
        return graph

    def _calc_result(self, calculated_graph):
        calc_dict: dict = self.__preparation_of_data_for_calculation(calculated_graph)
        # dataset_result: dict = self.__data_processing(calc_string=calc_string)
        # self.__processing_of_calculation_results(dataset_result)

    def __preparation_of_data_for_calculation(self, calculated_graph):
        calc_formula_dict = {}
        for field_symbol in calculated_graph:
            if '@' in field_symbol:  # todo не придется проверять переделать парсер
                current_field = self.__data[field_symbol]
                calc_formula_dict.update({
                    current_field._symbol:
                        self.__parser_manager.parameter_for_calculating_the_result(
                            formula_string=current_field.formula)
                })
        print(calc_formula_dict)
        return calc_formula_dict

    # def _calc_result(self, calculated_graph):
    #     for param in calculated_graph:
    #         if '@' in param:  # переменная
    #             current_field = self.__data[param]
    #             self._result.update({param: self.__calculation(current_field)})
    #         else:  # не формула
    #             self._result.update({param: float(param)})

    # def __calculation(self, current_field):
    #     current_field.prepare_calc(fields_values_dict=self._result)  # Обновляет value внутри field
    #     current_field.calc()
    #     return current_field._value
