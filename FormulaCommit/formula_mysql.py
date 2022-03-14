from abc import ABC, abstractmethod


class AbstractFormula(ABC):

    def __init__(self):
        self.delimiter = ''
        self.count_param = 0  # Парсер заполнит количество элементов сам

    @abstractmethod
    def get_transformation(self, *args, **kwargs):
        pass


class AggregateMysqlFormula(AbstractFormula):  # Агрегирующая формула
    """
    Стандартная формула mysql, для рассчета необходимо передать именованный аргумент формулы в функцию
    get_transformation, пример: get_transformation(args, assay_number=n, formula_name='avg')
    """

    def get_transformation(self, args, *, assay_number, formula_name):
        return f'(select {formula_name}(t.result) from(' + \
               ' union '.join([f'select {args}_{number} as result' for number in assay_number]) \
               + ') as t)'


class AggregateSqliteFormula(AbstractFormula):  # Агрегирующая формула
    """
    Стандартная формула mysql, для рассчета необходимо передать именованный аргумент формулы в функцию
    get_transformation, пример: get_transformation(args, assay_number=n, formula_name='avg')
    """

    def get_transformation(self, args, *, assay_number, formula_name):
        if assay_number:
            return f'(select {formula_name}(t.result) from (' + \
                   ' union '.join([f'select {args}_{number} as result from variable' for number in assay_number]) \
                   + ') as t)'
        else:
            return '(null)'


class FormulaOnlyMySQL(AbstractFormula):

    def __init__(self):
        super().__init__()
        self.delimiter = ','

    def get_transformation(self, *args, **kwargs):
        if kwargs['assay_number']:
            return '(select if(count(t.result)>1, ' \
                   f'{f"{args[2]}, {args[1]}" if len(args) == 3 else f"{args[1]}, t.result"}) from(' + \
                   ' union '.join([f'select distinct {args[0]}_{assay_number} as result'
                                   for assay_number in kwargs['assay_number']]) \
                   + ') as t)'
        else:
            return "(null)"


class FormulaOnlySqlite(AbstractFormula):

    def __init__(self):
        super().__init__()
        self.delimiter = ','

    def get_transformation(self, *args, **kwargs):
        if kwargs['assay_number']:  # todo проверить как работает, вроде уже устранил ошибку
            return '(select CASE WHEN count(t.result)>1 then ' \
                   f'{f"{args[2]} else {args[1]}" if len(args) == 3 else f"{args[1]} else t.result"} end from (' + \
                   ' union '.join([f'select distinct {args[0]}_{assay_number} as result'
                                   for assay_number in kwargs['assay_number']]) \
                   + ') as t)'
        else:
            return "(null)"


class FormulaIFSqlite(AbstractFormula):

    def __init__(self):
        super().__init__()
        self.delimiter = ','

    def get_transformation(self, *args, **kwargs):
        return f'(SELECT CASE WHEN {args[0]} THEN {args[1]} ELSE {args[2]}  END)'
