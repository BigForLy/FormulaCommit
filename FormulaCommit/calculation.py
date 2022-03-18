from abc import ABC, abstractmethod

from FormulaCommit.db_module import SqliteConnectionUsingMemoryFactory, \
    MySQLConnectionFactory
from FormulaCommit.definition_manager import DefinitionFactory, DefinitionFactoryMysql, DefinitionFactorySqlite
from FormulaCommit.parse_sql import ParserMySQLFactory, ParserSqliteFactory


class AbstractCalculationMethod(ABC):
    """
    Абстрактный класс расчетного метода

    Methods
    -------
    calc_result
    """

    @abstractmethod
    def calc_result(self, symbol_and_calculate_item_list) -> dict:
        """
        Вычисление результата, включает парсер параметров и расчет значений
        :param symbol_and_calculate_item_list:
        :return:
        """
        pass


class CalculationMethodForMySql(AbstractCalculationMethod):

    def calc_result(self, symbol_and_calculate_item_list) -> dict:
        parser = ParserMySQLFactory().parser()
        calc_string, select_string = parser.parse(symbol_and_calculate_item_list)
        connect = MySQLConnectionFactory().connect()
        dataset_result = connect.calculator(calc_string, select_string)
        return dataset_result


class CalculationMethodForSqlite(AbstractCalculationMethod):

    def calc_result(self, symbol_and_calculate_item_list) -> dict:
        parser = ParserSqliteFactory().parser()
        calc_string, select_string = parser.parse(symbol_and_calculate_item_list)
        connect = SqliteConnectionUsingMemoryFactory().connect()
        dataset_result = connect.calculator(calc_string, select_string)
        return dataset_result


class AbstractCalculationFactory(ABC):
    """
    Фабрика расчетного менеджера

    Methods
    -------
    calculation_method
    definition_manager
    """

    @abstractmethod
    def calculation_method(self) -> AbstractCalculationMethod:
        """

        :return: экземпляр класса расчетного метода AbstractCalculationMethod
        """
        pass

    @abstractmethod
    def definition_manager(self) -> DefinitionFactory:
        """

        :return: экземпляр класса менеджера определений AbstractDefinition
        """
        pass


class CalculationFactoryMySql(AbstractCalculationFactory):

    def calculation_method(self) -> AbstractCalculationMethod:
        return CalculationMethodForMySql()

    def definition_manager(self) -> DefinitionFactory:
        return DefinitionFactoryMysql()


class CalculationFactorySqlite(AbstractCalculationFactory):

    def calculation_method(self) -> AbstractCalculationMethod:
        return CalculationMethodForSqlite()

    def definition_manager(self) -> DefinitionFactory:
        return DefinitionFactorySqlite()
