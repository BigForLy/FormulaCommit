from FormulaCommit.formula.formula import AbstractFormula


class AggregateMysqlFormula(AbstractFormula):  # Агрегирующая формула
    """
    Стандартная формула mysql, для рассчета необходимо передать именованный аргумент формулы в функцию
    get_transformation, пример: get_transformation(args, assay_number=n, formula_name='avg')
    """

    def get_transformation(self, args, *, definition_number, formula_name, number_field_by_symbol):
        assay_number = number_field_by_symbol.get(args)
        if assay_number:
            return f'(select {formula_name}(t.result) from(' + \
                   ' union '.join([f'select {args}_{number} as result' for number in assay_number]) \
                   + ') as t)'
        else:
            return '(null)'


class FormulaOnlyMySQL(AbstractFormula):

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
            else:
                tmp_params.append(token)
        if tmp_params:
            params.append(''.join(tmp_params))
        assay_number = kwargs["number_field_by_symbol"].get(params[0])
        if assay_number:
            return '(select if(count(t.result)>1, ' \
                   f'{f"{params[2]}, {params[1]}" if len(params) == 3 else f"{params[1]}, t.result"}) from(' + \
                   ' union '.join([f'select distinct {params[0]}_{assay_number} as result'
                                   for assay_number in assay_number]) \
                   + ') as t)'
        else:
            return "(null)"
