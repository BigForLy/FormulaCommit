from abc import abstractmethod, ABC
from dataclasses import dataclass

from FormulaCommit.formula_mysql import FormulaOnly, AggregateMysqlFormula, AggregateSqliteFormula


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
        stack = self.__separation_into_all_param(parsed_formula)
        return self.__update_func_param(stack, definition_number, number_field_by_symbol)

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
            if token in self._func:
                stack.append(token)
                self.isFormula = self._func[token]
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

    def __update_func_param(self, stack, definition_number, number_field_by_symbol):
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
            if x in self._func:
                param = []
                current_func = self._func[x]
                for i in range(current_func.count_param):
                    param.append(stack.pop())
                if number_field_by_symbol.get(param[0]):
                    func_result = current_func.get_transformation(*param,
                                                                  assay_number=number_field_by_symbol.get(param[0]),
                                                                  formula_name=x)
                else:
                    func_result = '(null)'
                yield func_result
            else:
                if '@' in x:
                    if '_' in x and x not in number_field_by_symbol:
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


class ParseMySQLManager(ParseSqlManager):

    def __init__(self):
        super().__init__()
        self._func = {'avg': AggregateMysqlFormula(),
                      'only': FormulaOnly(),
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
                      # 'only': FormulaOnly(),
                      'max': AggregateSqliteFormula(),
                      'min': AggregateSqliteFormula(),
                      'sum': AggregateSqliteFormula(),
                      'count': AggregateSqliteFormula()}

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
        column_variable = '"' + '", "'.join(list(map(lambda x: x[1].symbol_and_definition,
                                                     symbol_and_calculate_item_list.items()))) + '"'
        calc_string = f'CREATE TEMP TABLE IF NOT EXISTS variable({column_variable}); insert into variable (' + column_variable \
                      + f') values ({", ".join(["null" for _ in symbol_and_calculate_item_list])}); ' \
                        f'{" ".join(calc_item_formula)};'
        select_string = ' select ' + ', '.join(
            list(map(lambda x: f'"""{x[1].symbol_and_definition}""", "{x[1].symbol_and_definition}"',
                     symbol_and_calculate_item_list.items()))) + ' from variable;'
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
