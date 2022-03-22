from FormulaCommit.formula.formula_mysql import AggregateMysqlFormula, FormulaOnlyMySQL
from FormulaCommit.parse.parse_sql import ParseSqlManager, CalculateItem, ParserCalculationItemToExecuteString, \
    AbstractParserFactory


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

    @staticmethod
    def parameter_for_calculating_the_result(*, current_field):
        term = current_field.formula if current_field.formula and not current_field._value_only else \
            current_field.get_value_by_type()
        current_field.before_update_component()
        return CalculateItem(current_field.symbol_item.symbol_and_definition,
                             current_field.formula is not None and current_field.formula != '' and
                             not current_field._value_only,
                             f'set {current_field.symbol_item.symbol_and_definition}:={term};',
                             current_field._formula.formula_update_value_component,
                             )


class ParserCalculationItemToExecuteStringMySQL(ParserCalculationItemToExecuteString):

    def parse(self, symbol_and_calculate_item_list: dict[str, CalculateItem]) -> (str, str):
        calc_string = ''
        for key, item in symbol_and_calculate_item_list.items():
            calc_string += f'{item.formula} ' \
                           f'set {key} := (select case when cast(sum({key}) as char) = {key} then {item.formula_and_component} ' \
                           f'else {key} end); '
        select_string = ' select ' + ', '.join(list(map(lambda x: x[1].symbol_and_definition,
                                                        symbol_and_calculate_item_list.items())))
        print(calc_string, select_string)
        return calc_string, select_string


class ParserMySQLFactory(AbstractParserFactory):

    def parser(self) -> ParserCalculationItemToExecuteString:
        return ParserCalculationItemToExecuteStringMySQL()
