from FormulaCommit.definition.definition_manager import DefinitionManager, DefinitionFactory
from FormulaCommit.parse.parse_mysql import ParseMySQLManager


class DefinitionManagerMySql(DefinitionManager):

    def __init__(self):
        super().__init__()
        self._parser_manager = ParseMySQLManager()


class DefinitionFactoryMysql(DefinitionFactory):

    def manager(self) -> DefinitionManager:
        return DefinitionManagerMySql()
