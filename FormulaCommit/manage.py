import graphlib

from FormulaCommit.parse import ParseManager


class FormulaManager:

    def __init__(self, data):
        self.__data = data
        self.__result = {}
        self.__parse_manager = ParseManager()

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
        graph = {}
        for key, field_class in self.__data.items():
            graph.update({key: field_class._get_dependence()})
            # graph.update({key: set(self.__parse_manager.parses(field_class))})

        calculated_graph = tuple(graphlib.TopologicalSorter(graph).static_order())

        for param in calculated_graph:
            if '@' in param:
                current_field = self.__data[param]
                self.__result.update({param: current_field.calc(self.__result)})
            else:
                self.__result.update({param: float(param)})

            # if '@' not in param:  # число
            #     self.__result.update({param: float(param)})
            # else:  # формула-строка
            #     self.__result.update({param: (eval(self.__parse_manager.calc(self.__data[param], self.__result)))})

        print(self.__result)
