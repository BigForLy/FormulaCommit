class ParseSqlManagerOld:

    def __init__(self, assay_count):
        self.__OPERATORS = {'+', '-', '*', '/'}
        self.__assay_count = tuple(f'{name + 1}' for name in range(assay_count))
        self.__func = {'avg': self.__formula_avg,
                       'only': self.__formula_only}
        self.isFormulaParam = False

    def dependence(self, current_field):
        return set(self.__parses(current_field.formula))

    def __parses(self, formula_string):
        param = ''
        for s in formula_string:
            if s == '@':
                param += s
                self.isFormulaParam = True
            elif self.isFormulaParam and (s in self.__OPERATORS or s in "( ,)"):
                yield param
                self.isFormulaParam = False
                param = ''
            elif self.isFormulaParam:
                param += s
        if param and self.isFormulaParam:
            yield param if self.isFormulaParam else param  # float(param)
        self.isFormulaParam = False

    def update_formula(self, current_field):
        if '@' in current_field._formula:
            return self.__update_formula_parameters_by_definition(formula_string=current_field._formula,
                                                                  opred=current_field._opred_number)
        else:
            return current_field._formula

# transform
    def __update_formula_parameters_by_definition(self, *, formula_string, opred):
        def foo():
            nonlocal param
            if self.isFormulaParam and '_' in param and param.split('_')[-1] in self.__assay_count:
                # если указан параметр конкретного пределения
                return param
            else:
                return f'{param}_{opred}' if self.isFormulaParam else param

        active_func = None
        param = ''
        calc_string = ''
        for s in formula_string:
            if s == '@':
                self.isFormulaParam = True
                param += s
            elif s in self.__OPERATORS or s in "( ,)":  # garbage
                calc_string += active_func(param) if active_func else foo() if param not in self.__func else ''
                active_func = self.__func[param] if param in self.__func.keys() else None
                param = ''
                calc_string += s
                self.isFormulaParam = False
            else:
                param += s
        calc_string += foo()
        self.isFormulaParam = False
        return calc_string

    @staticmethod
    def parameter_for_calculating_the_result(*, field_symbol, formula_string, value):
        term = formula_string if formula_string else f"\"{str(value)}\""
        return f'set {field_symbol}:={term};'

    def __formula_avg(self, param):
        return 'select avg(t.result) from(' + \
               ' union '.join([f'select {param}_{assay_number} as result' for assay_number in self.__assay_count]) + \
               ') as t'

    def __formula_only(self, param, *args):
        return f'select if(count(*)>1, \"{args[0]}\", t.result) from(' + \
               ' union '.join([f'select {param}_{assay_number} as result' for assay_number in self.__assay_count]) + \
               ') as t'
