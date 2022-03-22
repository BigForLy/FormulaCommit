from FormulaCommit.calculation.calculation import AbstractCalculationMethod, AbstractCalculationFactory
from FormulaCommit.db_module.db_sqlite import SqliteConnectionUsingMemoryFactory
from FormulaCommit.definition.definition_manager import DefinitionFactory
from FormulaCommit.definition.definition_sqlite import DefinitionFactorySqlite
from FormulaCommit.parse.parse_sqlite import ParserSqliteFactory


class CalculationMethodForSqlite(AbstractCalculationMethod):

    def calc_result(self, symbol_and_calculate_item_list) -> dict:
        parser = ParserSqliteFactory().parser()
        calc_string, select_string = parser.parse(symbol_and_calculate_item_list)
        connect = SqliteConnectionUsingMemoryFactory().connect()
        dataset_result = connect.calculator(calc_string, select_string)
        return dataset_result


class CalculationFactorySqlite(AbstractCalculationFactory):

    def calculation_method(self) -> AbstractCalculationMethod:
        return CalculationMethodForSqlite()

    def definition_manager(self) -> DefinitionFactory:
        return DefinitionFactorySqlite()
