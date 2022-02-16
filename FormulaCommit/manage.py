import graphlib

from sqlalchemy import text

from FormulaCommit.parse import ParsePythonManager
from FormulaCommit.parse_sql import ParseSqlManager


class FormulaManager:

    def __init__(self, data):
        self.__data = data
        self.__result = {}

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

    @staticmethod
    def __calculated_graph(graph):
        return tuple(graphlib.TopologicalSorter(graph).static_order())

    def calc_python(self):
        graph = {}
        for key, field_class in self.__data.items():
            field_class._independent_parser_manager = ParsePythonManager()
            graph.update({key: field_class.dependence})

        calculated_graph = self.__calculated_graph(graph)

        for param in calculated_graph:
            if '@' in param:  # переменная
                current_field = self.__data[param]
                self.__result.update({param: current_field.calc(self.__result)})
            else:
                self.__result.update({param: float(param)})

        print(self.__result)

    def calc_mysql(self, session):
        graph = self.__collects_data_for_graph_mysql()

        calculated_graph = self.__calculated_graph(graph)

        calc_string = self.__prepare_formula_to_string_mysql(calculated_graph)

        return self.__data_processing_mysql(session=session, calc_string=calc_string)

    def __prepare_formula_to_string_mysql(self, calculated_graph):
        calc_formula_list = []
        for field_symbol in calculated_graph:
            current_field = self.__data[field_symbol]
            calc_formula_list.append(
                f"{field_symbol} := {current_field.calc(self.__result)} as \"{field_symbol}\"")  # todo можно вернуть формулу, убрать todo если переделаю на интерфейс

        calc_string = 'select ' + ', '.join(calc_formula_list)
        print(calc_string)
        return calc_string

    def __collects_data_for_graph_mysql(self):
        graph = {}
        for key, field_class in self.__data.items():
            # field_class._independent_parser_manager = ParseSqlManager()
            graph.update({key: field_class.dependence})
        return graph

    def __data_processing_mysql(self, session, calc_string):
        dataset = session.execute(text(calc_string)).all()
        self.__result = dict(dataset[0]._mapping)
        return self.__result


