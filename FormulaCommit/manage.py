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
        for key, value in self.__data.items():
            graph.update({key: set(self.__parse_manager.parses(value))})

        calculated_graph = tuple(graphlib.TopologicalSorter(graph).static_order())

        for param in calculated_graph:
            if param.find('@') == -1:  # число
                self.__result.update({param: float(param)})
            else:  # строка
                self.__result.update({param: float(eval(self.__parse_manager.calc(self.__data[param], self.__result)))})

        print(self.__result)


data = {"@d": "@a**@c",
        "@ab": "@d+@c",
        "@e": "round(@z, int(1))",
        "@z": "@a+@ab",
        "@a": "5.4",
        "@b": "10",
        "@c": "@a+@b"}


FormulaManager(data).calc()
