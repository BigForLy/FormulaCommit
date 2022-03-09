from abc import ABC, abstractmethod


class AbstractFormula(ABC):

    def __init__(self):
        self.delimiter = ''
        self.count_param = 0  # Парсер заполнит количество элементов сам

    @abstractmethod
    def get_transformation(self, *args, **kwargs):
        pass


class StandardFormula(AbstractFormula):
    """
    Стандартная формула mysql, для рассчета необходимо передать именованный аргумент формулы в функцию
    get_transformation, пример: get_transformation(args, assay_number=n, formula_name='avg')
    """

    def get_transformation(self, args, *, assay_number, formula_name):
        return f'(select {formula_name}(t.result) from(' + \
               ' union '.join([f'select {args}_{assay_number} as result' for assay_number in assay_number])\
               + ') as t)'


class FormulaOnly(AbstractFormula):

    def __init__(self):
        super().__init__()
        self.delimiter = ','

    def get_transformation(self, *args, **kwargs):
        return f'(select if(count(t.result)>1, {f"{args[2]}, {args[1]}" if len(args) == 3 else f"{args[1]}, t.result"}) from(' + \
               ' union '.join([f'select distinct {args[0]}_{assay_number} as result'
                               for assay_number in kwargs['assay_count']]) \
               + ') as t)'


class Formula:  # todo переделать в dataclass перенести в fields

    def __init__(self, formula):
        self.__formula = formula
        self.__dependence = set()

    @property
    def formula(self):
        return self.__formula

    @formula.setter
    def formula(self, value):
        self.__formula = value

    @property
    def dependence(self):
        return self.__dependence

    @dependence.setter
    def dependence(self, value):
        self.__dependence = value
