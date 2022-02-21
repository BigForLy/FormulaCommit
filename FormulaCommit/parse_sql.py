class ParseSqlManager:

    def __init__(self):
        self.__OPERATORS = {'+', '-', '*', '/'}
        self.isString = False

    def parses(self, formula_string):
        self.isString = False
        param = ''
        for s in formula_string:
            if s == '@':
                param += s
                self.isString = True
            elif self.isString and (s in self.__OPERATORS or s in "( ,)"):
                yield param
                self.isString = False
                param = ''
            elif self.isString:
                param += s
        if param and self.isString:
            yield param if self.isString else param  # float(param)

    @staticmethod
    def prepare_calc(*, field_symbol, formula_string):
        return f"set {field_symbol}:={formula_string};"  #  as \"{field_symbol}\"
