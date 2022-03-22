from FormulaCommit.definition.definition_manager import DefinitionManager, DefinitionFactory
from FormulaCommit.parse.parse_sqlite import ParseSqliteManager


class DefinitionManagerSqlite(DefinitionManager):

    def __init__(self):
        super().__init__()
        self._parser_manager = ParseSqliteManager()


class DefinitionFactorySqlite(DefinitionFactory):

    def manager(self) -> DefinitionManager:
        return DefinitionManagerSqlite()
