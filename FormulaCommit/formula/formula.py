from abc import ABC, abstractmethod


class AbstractFormula(ABC):

    def __init__(self):
        self.delimiter = ''
        self.count_param = 0  # Парсер заполнит количество элементов сам

    @abstractmethod
    def get_transformation(self, *args, **kwargs):
        pass



