from FormulaCommit.formula_mysql import FormulaAvg, FormulaOnly


class ParseSqlManager:

    def __init__(self, assay_count):
        self.__OPERATORS = {'+', '-', '*', '/'}
        self.__assay_count = tuple(f'{name + 1}' for name in range(assay_count))
        self.isFormula = None
        self.__func = {'avg': FormulaAvg(), 'only': FormulaOnly()}

    def update_formula(self, current_field):
        """
        Изменяет формулу для расчета
        :param current_field: рассчитываемое поле
        :type current_field: AbstractField
        :return: формула
        """
        if current_field.formula:
            all_param_generator = self.__parse(current_field.formula)
            formula_list = self.shunting_yard(all_param_generator, current_field)
            return ''.join(list(formula_list))
        else:
            return ''

    def __parse(self, formula_string):
        """
        Разделяет параметры на отдельные элементы при помощи разделителей из garbage
        :param formula_string: изначальная формула поля
        :type formula_string: str
        :return: список элементов изначальной формулы в виде генератора
        """
        param = ''
        for s in formula_string:
            if s in self.__OPERATORS or s in "( ,)":  # garbage
                if param:
                    yield param
                yield s
                param = ''
            else:
                param += s
        if param:
            yield param

    def shunting_yard(self, parsed_formula, current_field):
        """
        Сортировочный станция, задача сортировочной станции обработать список элементов изначальной формулы,
        превратить его в новый список удобочитаемых и используемых для функций элементов,
        преобразовать функции в формулы для вычислений в MySQL,
        обновить список зависимостей у поля после всех преобразований
        :param parsed_formula: список элементов изначальной формулы
        :type parsed_formula: generator
        :param current_field: рассчитываемое поле
        :type current_field: AbstractField
        :return: последовательный список параметров формулы для расчета в виде генератора
        """
        stack = self.__separation_into_all_param(parsed_formula)
        return self.__update_func_param(stack, current_field)

    def __separation_into_all_param(self, parsed_formula):
        """
        Преобразует список элементов изначальной формулы в новый список удобочитаемых и используемых для функций
        элементов
        :param parsed_formula: список элементов изначальной формулы
        :type parsed_formula: generator
        :return: обновленный список элементов используемый для функций и расчета
        """
        stack = []
        for token in parsed_formula:
            if token in self.__func:
                stack.append(token)
                self.isFormula = self.__func[token]
            elif token == ")":
                if self.isFormula:
                    ready_params_for_formula = []
                    temporary_params = []
                    while stack:
                        x = stack.pop()
                        if x == "(":
                            if temporary_params:
                                foo = ''.join(temporary_params[::-1])
                                temporary_params.clear()
                                ready_params_for_formula.append(foo)
                            break
                        elif x == self.isFormula.delimiter:
                            foo = ''.join(temporary_params[::-1])
                            temporary_params.clear()
                            ready_params_for_formula.append(foo)
                        else:
                            temporary_params.append(x)
                    if temporary_params:
                        foo = ''.join(temporary_params[::-1])
                        temporary_params.clear()
                        ready_params_for_formula.append(foo)
                    self.isFormula.count_param = len(ready_params_for_formula)
                    stack += ready_params_for_formula[::-1]
                else:
                    stack.append(token)
                self.isFormula = None
            elif token == "(":
                stack.append(token)
            else:
                stack.append(token)
        return stack[::-1]

    def __update_func_param(self, stack, current_field):
        """
        Добавляет номер определения для символьных обозначений полей в формуле,
        преобразовывает функции в формулы для вычислений в MySQL,
        обновляет список зависимостей у поля после всех преобразований
        :param stack: стек элементов для расчета
        :type stack: list
        :param current_field: рассчитываемое поле
        :type current_field: AbstractField
        :return: последовательный список параметров формулы для расчета в виде генератора
        """
        dependence_list = []  # todo можно усовершенствовать, если убрать добавление повторяющихся полей
        while stack:
            x = stack.pop()
            if x in self.__func:
                param = []
                current_func = self.__func[x]
                for i in range(current_func.count_param):
                    param.append(stack.pop())
                func_result = current_func.get_transformation(*param, assay_count=self.__assay_count)
                [dependence_list.append(parameter_for_formula) for parameter_for_formula in self.__parse(func_result)
                 if '@' in parameter_for_formula]
                yield func_result
            else:
                if '@' in x:
                    if '_' in x and x.split('_')[-1] in self.__assay_count:
                        now_x = x
                    else:
                        now_x = f'{x}_{current_field._opred_number}'
                    dependence_list.append(now_x)
                    yield now_x
                else:
                    yield x
        self.__update_dependence_by_field(current_field, dependence_list)

    @staticmethod
    def __update_dependence_by_field(current_field, dependence):
        current_field.dependence = set(dependence)

    @staticmethod
    def parameter_for_calculating_the_result(*, field_symbol, formula_string, value):
        term = formula_string if formula_string else f"\"{str(value)}\""
        return f'set {field_symbol}:={term};'

    # def shunting_yard(self, parsed_formula):
    # stack = []
    # for token in parsed_formula:
    #     if token in self.__func:
    #         stack.append(token)
    #         self.isFormula = self.__func[token]
    #     elif token == ")":
    #         if self.isFormula:
    #             ready_params_for_formula = []
    #             temporary_params = []
    #             while stack:
    #                 x = stack.pop()
    #                 if x == "(":
    #                     if temporary_params:
    #                         foo = ''.join(temporary_params[::-1])
    #                         temporary_params.clear()
    #                         ready_params_for_formula.append(foo)
    #                     break
    #                 elif x == self.isFormula.delimiter:
    #                     foo = ''.join(temporary_params[::-1])
    #                     temporary_params.clear()
    #                     ready_params_for_formula.append(foo)
    #                 else:
    #                     temporary_params.append(x)
    #             if temporary_params:
    #                 foo = ''.join(temporary_params[::-1])
    #                 temporary_params.clear()
    #                 ready_params_for_formula.append(foo)
    #             self.isFormula.count_param = len(ready_params_for_formula)
    #             stack += ready_params_for_formula[::-1]
    #         else:
    #             stack.append(token)
    #         self.isFormula = None
    #     elif token == "(":
    #         stack.append(token)
    #     else:
    #         stack.append(token)
    # stack = stack[::-1]
    # dependence_list = []
    # while stack:
    #     x = stack.pop()
    #     if x in self.__func:
    #         param = []
    #         current_func = self.__func[x]
    #         for i in range(current_func.count_param):
    #             param.append(stack.pop())
    #         func_result = current_func.get_transformation(*param, assay_count=self.__assay_count)
    #         [dependence_list.append(parameter_for_formula) for parameter_for_formula in self.__parse(func_result)
    #                                                         if '@' in parameter_for_formula]
    #         yield func_result
    #     else:
    #         if '@' in x:
    #             if '_' in x and x.split('_')[-1] in self.__assay_count:
    #                 now_x = x
    #             else:
    #                 now_x = f'{x}_{self.current_field._opred_number}'
    #             dependence_list.append(now_x)
    #             yield now_x
    #         else:
    #             yield x
    # self.current_field.dependence = set(dependence_list)  # выделить в отдельную функцию

    # def __formula_avg(self, param):
    #     return 'select avg(t.result) from(' + \
    #            ' union '.join([f'select {param}_{assay_number} as result' for assay_number in self.__assay_count]) + \
    #            ') as t'
    #
    # def __formula_only(self, param, *args):
    #     return f'select if(count(*)>1, \"{args[0]}\", t.result) from(' + \
    #            ' union '.join([f'select {param}_{assay_number} as result' for assay_number in self.__assay_count]) + \
    #            ') as t'
