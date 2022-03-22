from abc import abstractmethod, ABC
from dataclasses import dataclass

from FormulaCommit.formula_mysql import AbstractFormula


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


@dataclass
class CalculateItem:
    symbol_and_definition: str
    is_formula: bool  # Если True то формула, если False то value
    formula: str  # переименовать
    formula_and_component: str  # переименовать


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


class ParserCalculationItemToExecuteString(ABC):

    @abstractmethod
    def parse(self, symbol_and_calculate_item_list) -> (str, str):
        pass


class AbstractParserFactory(ABC):

    @abstractmethod
    def parser(self) -> ParserCalculationItemToExecuteString:
        pass
