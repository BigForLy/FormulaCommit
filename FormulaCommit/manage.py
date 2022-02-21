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
        data_result = self.__data_processing_mysql(session=self.__session, calc_string=calc_string)
        self.__post_processing(data_result)

    def __prepare_formula_to_string_mysql(self, calculated_graph):
        calc_formula_list = []
        for field_symbol in calculated_graph:
            current_field = self.__data[field_symbol]
            calc_formula_list.append(self.__calculation(current_field))

        calc_string = ' '.join(calc_formula_list)
        print(calc_string)
        return calc_string

    @staticmethod
    def __calculation(current_field):
        current_field.prepare_calc()  # Обновляет value внутри field
        return current_field._value  # тут формула mysql

    def __data_processing_mysql(self, session, calc_string):
        session.execute(text(calc_string))
        dataset = session.execute(text('select ' + ', '.join(self.__data.keys()))).all()
        return dataset[0]._mapping

    def __post_processing(self, data_result):
        for key, field_class in self.__data.items():
            # current_field = self.__data[key]
            field_class._value = data_result.get(key)
            self._result.update({key: field_class.calc()})


class FormulaManagerPython(AbstractFormulaManager):

    def __init__(self, data):
        super().__init__()
        self.__data = data
        self._result = {}
        # self.__parser_manager = ParsePythonManager()

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
            else:  # не формула
                self._result.update({param: float(param)})

    def __calculation(self, current_field):
        current_field.prepare_calc(fields_values_dict=self._result)  # Обновляет value внутри field
        current_field.calc()
        return current_field._value

