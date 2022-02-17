import graphlib

from sqlalchemy import text

from FormulaCommit.parse import ParsePythonManager
from FormulaCommit.parse_sql import ParseSqlManager


class AbstractFormulaManager:

    def __init__(self):
        self.__data = None
        self._result = {}

    @staticmethod
    def __to_fixed_range(number, digit=0):  # todo: Переименовать
        """
        Округление перед выводом пользователю, позволяет дополнить нулями значение
        Использует округление в большую сторону, применять для проставления нулей
        :param number: not str object
        :param digit: количество знаков после запятой
        :return: значение с определенным количеством знаков после запятой
        """
        return f"{number:.{digit}f}"

    def calc(self):
        graph = self._collects_data_for_graph()

        calculated_graph = self._calculated_graph(graph)

        self._calc_result(calculated_graph)

        return self._result

    @staticmethod
    def _calculated_graph(graph):
        return tuple(graphlib.TopologicalSorter(graph).static_order())

    @staticmethod
    def _collects_data_for_graph():
        return None

    @staticmethod
    def _calc_result(calculated_graph):
        pass

    # def calc_python(self):
    #     graph = {}
    #     for key, field_class in self.__data.items():
    #         field_class._independent_parser_manager = ParsePythonManager()
    #         graph.update({key: field_class.dependence})
    #
    #     calculated_graph = self._calculated_graph(graph)
    #
    #     for param in calculated_graph:
    #         if '@' in param:  # переменная
    #             current_field = self.__data[param]
    #             self._result.update({param: current_field.calc(self._result)})
    #         else:
    #             self._result.update({param: float(param)})
    #
    #     print(self._result)


class FormulaManagerMySql(AbstractFormulaManager):

    def __init__(self, data, session):
        super().__init__()
        self.__data = data
        self.__session = session
        self._result = {}

    def _collects_data_for_graph(self):
        graph = {}
        for key, field_class in self.__data.items():
            field_class._independent_parser_manager = ParseSqlManager()
            graph.update({key: field_class.dependence})
        return graph

    def _calc_result(self, calculated_graph):
        calc_string = self.__prepare_formula_to_string_mysql(calculated_graph)
        self.__data_processing_mysql(session=self.__session, calc_string=calc_string)

    def __prepare_formula_to_string_mysql(self, calculated_graph):
        calc_formula_list = []
        for field_symbol in calculated_graph:
            current_field = self.__data[field_symbol]
            calc_formula_list.append(
                f"{field_symbol} := {self.__calculation(current_field)} as \"{field_symbol}\"")  # todo можно вернуть формулу, убрать todo если переделаю на интерфейс

        calc_string = 'select ' + ', '.join(calc_formula_list)
        print(calc_string)
        return calc_string

    @staticmethod
    def __calculation(current_field):
        return current_field._formula

    def __data_processing_mysql(self, session, calc_string):
        dataset = session.execute(text(calc_string)).all()
        self._result = dict(dataset[0]._mapping)


class FormulaManagerPython(AbstractFormulaManager):

    def __init__(self, data):
        super().__init__()
        self.__data = data
        self._result = {}

    def _collects_data_for_graph(self):
        graph = {}
        for key, field_class in self.__data.items():
            field_class._independent_parser_manager = ParsePythonManager()
            graph.update({key: field_class.dependence})
        return graph

    def _calc_result(self, calculated_graph):
        for param in calculated_graph:
            if '@' in param:  # переменная
                current_field = self.__data[param]
                # self._result.update({param: current_field.calc(self._result)})
                self._result.update({param: self.__calculation(current_field)})
            else:
                self._result.update({param: float(param)})

    def __calculation(self, current_field):
        # def calc(self, formula_string, field_value_dict):
        self.isString = False
        element = ''
        calc_string = ''
        for s in current_field._formula:
            if s in '1234567890.' and not self.isString:  # number
                element += s
            elif s in self.__OPERATORS or s in "( ,)":  # garbage
                if element:
                    calc_string += self._result[element] if self._result.get(
                        element) and self.isString else element
                    element = ''
                calc_string += s
                self.isString = False
            else:  # string
                self.isString = True
                element += s
        if element:
            calc_string += str(self._result[element]) if self._result.get(element) and self.isString else element
        return calc_string
