from FormulaCommit.formula_mysql import FormulaOnlySqlite, AggregateSqliteFormula, FormulaIFSqlite
from FormulaCommit.parse.parse_sql import ParseSqlManager, CalculateItem, ParserCalculationItemToExecuteString, \
    AbstractParserFactory


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

    @staticmethod
    def parameter_for_calculating_the_result(*, current_field):
        term = current_field.formula if current_field.formula and not current_field._value_only else \
            f"\"{str(current_field._value)}\""
        current_field._formula.formula_update_value_component = f'"{current_field._formula.formula_update_value_component}"'
        current_field.before_update_component()
        return CalculateItem(current_field.symbol_item.symbol_and_definition,
                             current_field.formula is not None and current_field.formula != '' and
                             not current_field._value_only,
                             f'{term}',
                             current_field._formula.formula_update_value_component
                             )


class ParserCalculationItemToExecuteStringSqlite(ParserCalculationItemToExecuteString):

    def parse(self, symbol_and_calculate_item_list) -> (str, str):
        calc_item_formula = []
        for key, item in symbol_and_calculate_item_list.items():
            calc_item_formula.append(
                f'update variable set "{key}"=(select {item.formula} from variable); '
                f'update variable set "{key}"= (select case when is_number("{key}") then {item.formula_and_component} '
                f'else "{key}" end  from variable);')
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


class ParserSqliteFactory(AbstractParserFactory):

    def parser(self) -> ParserCalculationItemToExecuteString:
        return ParserCalculationItemToExecuteStringSqlite()
