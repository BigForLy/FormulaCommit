import graphlib

from FormulaCommit.parse import ParseManager


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

    def calc(self):
        graph = {}
        for key, field_class in self.__data.items():
            graph.update({key: field_class.dependence})

        calculated_graph = tuple(graphlib.TopologicalSorter(graph).static_order())

        for param in calculated_graph:
            if '@' in param:
                current_field = self.__data[param]
                self.__result.update({param: current_field.calc(self.__result)})
            else:
                self.__result.update({param: float(param)})

        print(self.__result)
