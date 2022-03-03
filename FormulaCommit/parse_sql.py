from FormulaCommit.formula_mysql import FormulaOnly, StandardFormula


class ParseSqlManager:

    def __init__(self, assay_count):
        self.__OPERATORS = {'+', '-', '*', '/'}
        self.__assay_count1 = tuple(f'{name + 1}' for name in range(assay_count))  # todo нужно отказаться
        self.number_field_by_symbol = {}
        self.isFormula = None
        self.__func = {'avg': StandardFormula(),  # todo не создавать экземпляр класса каждый раз
                       'only': FormulaOnly(),
                       'max': StandardFormula(),
                       'min': StandardFormula(),
                       'sum': StandardFormula(),
                       'count': StandardFormula()}

    def update_formula(self, current_field):
        """
        Изменяет формулу для расчета
        :param current_field: рассчитываемое поле
        :type current_field: AbstractField
        :return: формула
        """
        if current_field.formula:
            all_param_generator = self.__parse(current_field.formula)
            formula_list = self.shunting_yard(all_param_generator, current_field._opred_number)
            return ''.join(list(formula_list))
        else:
            return ''

    def update_dependence(self, current_field):
        """
        Рассчитывает список зависимостей у формулы
        :param current_field: рассчитываемое поле
        :type current_field: AbstractField
        :return: множество зависимостей у формулы поля
        """
        return set(x for x in self.__parse(current_field.formula) if '@' in x)

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

    def shunting_yard(self, parsed_formula, definition_number):
        """
        Сортировочный станция, задача сортировочной станции обработать список элементов изначальной формулы,
        превратить его в новый список удобочитаемых и используемых для функций элементов,
        преобразовать функции в формулы для вычислений в MySQL
        :param parsed_formula: список элементов изначальной формулы
        :type parsed_formula: generator
        :param definition_number: номер определения поля рассчета
        :type definition_number: int
        :return: последовательный список параметров формулы для расчета в виде генератора
        """
        stack = self.__separation_into_all_param(parsed_formula)
        return self.__update_func_param(stack, definition_number)

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

    def __update_func_param(self, stack, definition_number):
        """
        Добавляет номер определения для символьных обозначений полей в формуле,
        преобразовывает функции в формулы для вычислений в MySQL
        :param stack: стек элементов для расчета
        :type stack: list
        :param definition_number: номер определения поля рассчета
        :type definition_number: int
        :return: последовательный список параметров формулы для расчета в виде генератора
        """
        while stack:
            x = stack.pop()
            if x in self.__func:
                param = []
                current_func = self.__func[x]
                for i in range(current_func.count_param):
                    param.append(stack.pop())
                func_result = current_func.get_transformation(*param, assay_number=self.number_field_by_symbol[param[0]],
                                                              formula_name=x)
                yield func_result
            else:
                if '@' in x:
                    if '_' in x and x not in self.number_field_by_symbol:
                        now_x = x
                    else:
                        now_x = f'{x}_{definition_number}'
                    yield now_x
                else:
                    yield x

    @staticmethod
    def parameter_for_calculating_the_result(*, current_field):
        term = current_field.formula if current_field.formula and not current_field._value_only else \
            f"\"{str(current_field._value)}\""
        return f'set {current_field._symbol}_{current_field._opred_number}:={term};'
