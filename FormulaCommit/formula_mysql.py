from abc import ABC, abstractmethod


class AbstractFormula(ABC):
    @abstractmethod
    def get_transformation(self, *args, **kwargs):
        pass


class FormulaAvg(AbstractFormula):

    def __init__(self):
        self.count_param = 1
        self.delimiter = ''

    def get_transformation(self, *args, **kwargs):
        return '(select avg(t.result) from(' + \
               ' union '.join([f'select {args[0]}_{assay_number} as result' for assay_number in kwargs['assay_count']])\
               + ') as t)'


class FormulaOnly(AbstractFormula):

    def __init__(self):
        self.count_param = 2 | 3
        self.delimiter = ','

    def get_transformation(self, *args, **kwargs):
        return '(select avg(t.result) from(' + \
               ' union '.join([f'select {args[0]}_{assay_number} as result' for assay_number in kwargs['assay_count']]) \
               + ') as t)'
