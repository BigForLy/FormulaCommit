from abc import abstractmethod, ABC
from dataclasses import dataclass

from FormulaCommit.formula_mysql import FormulaOnlyMySQL, AggregateMysqlFormula, AggregateSqliteFormula, \
    FormulaOnlySqlite, FormulaIFSqlite, AbstractFormula


class ParseSqlManager(ABC):

    def __init__(self):
        self.__OPERATORS = {'+', '-', '*', '/'}
        self.isFormula = None
        self._func = None

    @abstractmethod
    def update_formula(self, current_field, number_field_by_symbol) -> str:
        """
        Изменяет формулу для расчета
        :param current_field: рассчитываемое поле
        :type current_field: AbstractField
        :return: формула
        """
        pass

    @abstractmethod
    def update_dependence(self, formula) -> set[str]:
        """
        Рассчитывает список зависимостей у формулы
        :param current_field: рассчитываемое поле
        :type current_field: AbstractField
        :return: множество зависимостей у формулы поля
        """
        pass

    def _parse(self, formula_string):
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

    def shunting_yard(self, parsed_formula, definition_number, number_field_by_symbol):
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
        stack = self.__separation_into_all_param(parsed_formula, definition_number, number_field_by_symbol)
        return stack

    def __separation_into_all_param(self, parsed_formula, definition_number, number_field_by_symbol):
        """
        Преобразует список элементов изначальной формулы в новый список удобочитаемых и используемых для функций
        элементов
        :param parsed_formula: список элементов изначальной формулы
        :type parsed_formula: generator
        :return: обновленный список элементов используемый для функций и расчета
        """
        stack_list: list[ParserItem] = [ParserItem(None, [], [], '', '')]
        parser_item = stack_list[-1]
        for token in parsed_formula:
            if token in self._func:
                stack_list.append(ParserItem(self._func[token], [], [], token, ''))
                parser_item = stack_list[-1]
            elif token == ")":
                parser_item.open_bracket -= 1
                if parser_item.open_bracket != 0:
                    parser_item.stack.append(token)
                    continue
                if parser_item.is_formula:
                    ready_params_for_formula = []
                    temporary_params = []
                    while parser_item.stack:
                        x = parser_item.stack.pop()
                        if x == "(" and not parser_item.stack:
                            if temporary_params:
                                foo = ''.join(temporary_params[::-1])
                                temporary_params.clear()
                                ready_params_for_formula.append(foo)
                            break
                        elif x == parser_item.is_formula.delimiter:
                            foo = ''.join(temporary_params[::-1])
                            temporary_params.clear()
                            if foo.replace(' ', ''):
                                ready_params_for_formula.append(foo)
                            ready_params_for_formula.append(parser_item.is_formula.delimiter)
                        elif '@' in x and x in number_field_by_symbol:
                            if temporary_params:
                                foo = ''.join(temporary_params[::-1])
                                temporary_params.clear()
                                ready_params_for_formula.append(foo)
                            ready_params_for_formula.append(x)
                            parser_item.params.append(x)
                        else:
                            temporary_params.append(x)
                    if temporary_params:
                        foo = ''.join(temporary_params[::-1])
                        temporary_params.clear()
                        ready_params_for_formula.append(foo)
                    parser_item.stack += ready_params_for_formula[::-1]
                    last_parser_item = stack_list.pop()
                    parser_item = stack_list[-1]
                    last_parser_item.calc(definition_number, number_field_by_symbol)
                    parser_item.stack.append(last_parser_item.result)
                else:
                    parser_item.stack.append(token)
            elif token == "(":
                parser_item.open_bracket += 1
                parser_item.stack.append(token)
            elif token == " " and parser_item.is_formula and len(parser_item.stack) == 0:
                pass
            else:
                parser_item.stack.append(token)
        assert len(stack_list) == 1
        parser_item.calc(definition_number, number_field_by_symbol)
        return parser_item.result

    def __unpacking(self, item):
        if isinstance(item, list):
            if len(item) == 1:
                return self.__unpacking(item[0])
            else:
                return item

    # def __update_func_param(self, stack, definition_number, number_field_by_symbol):
    #     """
    #     Добавляет номер определения для символьных обозначений полей в формуле,
    #     преобразовывает функции в формулы для вычислений в MySQL
    #     :param stack: стек элементов для расчета
    #     :type stack: list
    #     :param definition_number: номер определения поля рассчета
    #     :type definition_number: int
    #     :return: последовательный список параметров формулы для расчета в виде генератора
    #     """
    #     if isinstance(stack, ParserItem) and stack.is_formula:
    #         current_func = stack.is_formula
    #         func_result = current_func.get_transformation(*stack.stack,
    #                                                       assay_number=number_field_by_symbol.get(stack.params[0]),
    #                                                       formula_name=stack.formula_name)
    #         yield func_result
    #     while stack:
    #         x = stack.pop()
    #         if isinstance(x, ParserItem):
    #             yield list(self.__update_func_param(x, definition_number, number_field_by_symbol))[0]
    #         if x in self._func:
    #             param = []
    #             current_func = self._func[x]
    #             for i in range(current_func.count_param):
    #                 item = stack.pop()
    #                 if isinstance(item, list):
    #                     item = list(self.__update_func_param(item, definition_number, number_field_by_symbol))[0]
    #                 param.append(item)
    #             param = self.__update_formula_param_by_delimiter(param, current_func.delimiter)
    #             func_result = current_func.get_transformation(*param,
    #                                                           assay_number=number_field_by_symbol.get(param[0]),
    #                                                           formula_name=x)
    #             yield func_result
    #         else:
    #             if '@' in x:
    #                 if '_' in x and x not in number_field_by_symbol:
    #                     now_x = x
    #                 else:
    #                     now_x = f'{x}_{definition_number}'
    #                 yield now_x
    #             else:
    #                 yield x

    # def __update_formula_param_by_delimiter(self, all_param, delimiter):
    #     param_delimiter = [[]]
    #     actual_param = param_delimiter[0]
    #     for i in all_param:
    #         if i == delimiter:
    #             param_delimiter.append([])
    #             actual_param = param_delimiter[len(param_delimiter) - 1]
    #         else:
    #             actual_param.append(i)
    #     return [''.join(x) for x in param_delimiter]

    @staticmethod
    def parameter_for_calculating_the_result(*, current_field):
        term = current_field.formula if current_field.formula and not current_field._value_only else \
            f"\"{str(current_field._value)}\""
        return CalculateItem(current_field.symbol_item.symbol_and_definition,
                             current_field.formula is not None and current_field.formula != '' and
                             not current_field._value_only,
                             f'set {current_field.symbol_item.symbol_and_definition}:={term};',
                             f'({term})',
                             )


@dataclass
class CalculateItem:
    symbol_and_definition: str
    is_formula: bool  # Если True то формула, если False то value
    formula_old: str  # Формула для mysql
    formula: str  # переименовать


@dataclass
class ParserItem:
    is_formula: AbstractFormula | None
    stack: list
    params: list
    formula_name: str
    result: str
    open_bracket: int = 0

    def calc(self, definition_number, number_field_by_symbol):
        if self.is_formula:
            self.result = self.is_formula.get_transformation(*self.stack,
                                                             definition_number=definition_number,
                                                             formula_name=self.formula_name,
                                                             number_field_by_symbol=number_field_by_symbol)
        else:
            params = []
            tmp_params = []
            for token in self.stack:
                if '@' in token and token in number_field_by_symbol:
                    tmp_params.append(f'{token}_{definition_number}')
                else:
                    tmp_params.append(token)
            if tmp_params:
                params.append(''.join(tmp_params))
            self.result = ''.join(params)


class ParseMySQLManager(ParseSqlManager):

    def __init__(self):
        super().__init__()
        self._func = {'avg': AggregateMysqlFormula(),
                      'only': FormulaOnlyMySQL(),
                      'max': AggregateMysqlFormula(),
                      'min': AggregateMysqlFormula(),
                      'sum': AggregateMysqlFormula(),
                      'count': AggregateMysqlFormula()}

    def update_formula(self, current_field, number_field_by_symbol) -> str:
        """
        Изменяет формулу для расчета
        :param current_field: рассчитываемое поле
        :type current_field: AbstractField
        :return: формула
        """
        all_param_generator = self._parse(current_field.formula)
        formula_list = self.shunting_yard(all_param_generator, current_field._definition_number, number_field_by_symbol)
        return ''.join(list(formula_list))

    def update_dependence(self, formula) -> set[str]:
        """
        Рассчитывает список зависимостей у формулы
        :param current_field: рассчитываемое поле
        :type current_field: AbstractField
        :return: множество зависимостей у формулы поля
        """
        return set(x for x in self._parse(formula) if '@' in x)


class ParseSqliteManager(ParseSqlManager):

    def __init__(self):
        super().__init__()
        self._func = {'avg': AggregateSqliteFormula(),  # todo переделать в хранитель ссылок на класс а не экземпляр
                      'only': FormulaOnlySqlite(),
                      'max': AggregateSqliteFormula(),
                      'min': AggregateSqliteFormula(),
                      'sum': AggregateSqliteFormula(),
                      'count': AggregateSqliteFormula(),
                      'if': FormulaIFSqlite()}

    def update_formula(self, current_field, number_field_by_symbol) -> str:
        """
        Изменяет формулу для расчета
        :param current_field: рассчитываемое поле
        :type current_field: AbstractField
        :return: формула
        """
        all_param_generator = self._parse(current_field.formula)
        formula_list = self.shunting_yard(all_param_generator, current_field._definition_number, number_field_by_symbol)
        formula_item = self._parse(''.join(list(formula_list)))
        formula_str = ''
        for item in formula_item:
            formula_str += f'"{item}"' if '@' in item else item
        return formula_str

    def update_dependence(self, formula) -> set[str]:
        """
        Рассчитывает список зависимостей у формулы
        :param current_field: рассчитываемое поле
        :type current_field: AbstractField
        :return: множество зависимостей у формулы поля
        """
        return set(x.replace('"', '') for x in self._parse(formula) if '@' in x)


class ParserCalculationItemToExecuteString(ABC):

    @abstractmethod
    def parse(self, symbol_and_calculate_item_list) -> (str, str):
        pass


class ParserCalculationItemToExecuteStringMySQL(ParserCalculationItemToExecuteString):

    def parse(self, symbol_and_calculate_item_list: dict[str, CalculateItem]) -> (str, str):
        calc_string = ' '.join(list(map(lambda x: x[1].formula_old, symbol_and_calculate_item_list.items())))
        select_string = ' select ' + ', '.join(list(map(lambda x: x[1].symbol_and_definition,
                                                        symbol_and_calculate_item_list.items())))
        print(calc_string, select_string)
        return calc_string, select_string


class ParserCalculationItemToExecuteStringSqlite(ParserCalculationItemToExecuteString):

    def parse(self, symbol_and_calculate_item_list) -> (str, str):
        calc_item_formula = []
        for _, item in symbol_and_calculate_item_list.items():
            calc_item_formula.append(
                f'update variable set "{item.symbol_and_definition}"=(select {item.formula} from variable);')
        list_symbol_and_definition = list(map(lambda x: x[1].symbol_and_definition,
                                              symbol_and_calculate_item_list.items()))
        column_variable = '"' + '", "'.join(list_symbol_and_definition) + '"'
        calc_string = f'CREATE TEMP TABLE IF NOT EXISTS variable({column_variable}); ' \
                      f'insert into variable ({column_variable}) ' \
                      f'values ({", ".join(["null" for _ in list_symbol_and_definition])}); ' \
                      f'{" ".join(calc_item_formula)}'
        select_string = ' select ' + ', '.join(
            list(map(lambda x: f'"""{x}""", "{x}"', list_symbol_and_definition))) + ' from variable;'
        print(calc_string, select_string)
        return calc_string, select_string


class AbstractParserFactory(ABC):

    @abstractmethod
    def parser(self) -> ParserCalculationItemToExecuteString:
        pass


class ParserMySQLFactory(AbstractParserFactory):

    def parser(self) -> ParserCalculationItemToExecuteString:
        return ParserCalculationItemToExecuteStringMySQL()


class ParserSqliteFactory(AbstractParserFactory):

    def parser(self) -> ParserCalculationItemToExecuteString:
        return ParserCalculationItemToExecuteStringSqlite()
