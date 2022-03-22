from FormulaCommit.formula.formula import AbstractFormula


class AggregateSqliteFormula(AbstractFormula):  # Агрегирующая формула
    """
    Стандартная формула mysql, для рассчета необходимо передать именованный аргумент формулы в функцию
    get_transformation, пример: get_transformation(args, assay_number=n, formula_name='avg')
    """

    def get_transformation(self, args, *, definition_number, formula_name, number_field_by_symbol):
        assay_number = number_field_by_symbol.get(args)
        if assay_number:
            return f'(select {formula_name}(t.result) from (' + \
                   ' union '.join([f'select {args}_{number} as result from variable' for number in assay_number]) \
                   + ') as t)'
        else:
            return '(null)'


class FormulaOnlySqlite(AbstractFormula):

    def __init__(self):
        super().__init__()
        self.delimiter = ','

    def get_transformation(self, *args, **kwargs):
        # todo разделить метод на 2, один где два параметра, второй где 3, вариант с полиморфизмом
        params = []
        tmp_params = []
        for token in args:
            if token == self.delimiter:
                params.append(''.join(tmp_params))
                tmp_params.clear()
            else:
                tmp_params.append(token)
        if tmp_params:
            params.append(''.join(tmp_params))
        assay_number = kwargs["number_field_by_symbol"].get(params[0])
        if assay_number:
            return '(select CASE WHEN count(t.result)>1 then ' \
                   f'{f"{params[2]} else {params[1]}" if len(params) == 3 else f"{params[1]} else t.result"} end from (' + \
                   ' union '.join([f'select distinct {params[0]}_{number} as result'
                                   for number in assay_number]) \
                   + ') as t)'
        else:
            return "(null)"


class FormulaIFSqlite(AbstractFormula):

    def __init__(self):
        super().__init__()
        self.delimiter = ','

    def get_transformation(self, *args, **kwargs):
        params = []
        tmp_params = []
        for token in args:
            if token == self.delimiter:
                params.append(''.join(tmp_params))
                tmp_params.clear()
            elif '@' in token and token in kwargs["number_field_by_symbol"]:
                tmp_params.append(f'{token}_{kwargs["definition_number"]}')
            else:
                tmp_params.append(token)
        if tmp_params:
            params.append(''.join(tmp_params))
        return f'(SELECT CASE WHEN {params[0]} THEN {params[1]} ELSE {params[2]}  END)'
