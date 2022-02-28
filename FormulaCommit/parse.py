class ParsePythonManager:

    def __init__(self):
        self.__OPERATORS = {'+', '-', '*', '/'}
        self.__func = {'round', 'int'}
        self.isString = False

    def dependence(self, current_field):
        return set(self.__parses(current_field._formula))

    def __parses(self, formula_string):
        self.isString = False
        param = ''
        for s in formula_string:
            if s in '1234567890.' and not self.isString:  # number
                param += s
            elif s in self.__OPERATORS or s in "( ,)":  # garbage
                if param and param in self.__func:
                    param = ''
                if param:
                    yield param if self.isString else param  # float(param)
                    param = ''
                self.isString = False
            else:  # string
                self.isString = True
                param += s
        if param:
            yield param if self.isString else param  # float(param)

    def parameter_for_calculating_the_result(self, *, formula_string):
        return f'{formula_string}'


    # def prepare_calc(self, *, formula_string, field_value_dict):
    #     self.isString = False
    #     param = ''
    #     calc_string = ''
    #     for s in formula_string:
    #         if s in '1234567890.' and not self.isString:  # number
    #             param += s
    #         elif s in self.__OPERATORS or s in "( ,)":  # garbage
    #             if param:
    #                 calc_string += f'({field_value_dict[param]})' if field_value_dict.get(
    #                     param) and self.isString else param
    #                 param = ''
    #             calc_string += s
    #             self.isString = False
    #         else:  # string
    #             self.isString = True
    #             param += s
    #     if param:
    #         calc_string += f'({field_value_dict[param]})' if field_value_dict.get(param) and self.isString else param
    #     return calc_string
