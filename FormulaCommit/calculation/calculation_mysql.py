from FormulaCommit.calculation.calculation import AbstractCalculationMethod, AbstractCalculationFactory
from FormulaCommit.db_module.db_mysql import MySQLConnectionFactory
from FormulaCommit.definition.definition_manager import DefinitionFactory
from FormulaCommit.definition.definition_mysql import DefinitionFactoryMysql
from FormulaCommit.parse.parse_mysql import ParserMySQLFactory


class CalculationMethodForMySql(AbstractCalculationMethod):

    def calc_result(self, symbol_and_calculate_item_list) -> dict:
        parser = ParserMySQLFactory().parser()
        calc_string, select_string = parser.parse(symbol_and_calculate_item_list)
        connect = MySQLConnectionFactory().connect()
        dataset_result = connect.calculator(calc_string, select_string)
        return dataset_result


class CalculationFactoryMySql(AbstractCalculationFactory):

    def calculation_method(self) -> AbstractCalculationMethod:
        return CalculationMethodForMySql()

    def definition_manager(self) -> DefinitionFactory:
        return DefinitionFactoryMysql()
