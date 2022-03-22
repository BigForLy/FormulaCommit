import datetime
import sqlite3
from types import NoneType

from FormulaCommit.db_module.db_module import Connection, AbstractConnectionFactory


class SqliteConnectionMemory(Connection):

    def calculator(self, calc_string, select_string) -> dict:
        foo = datetime.datetime.now()

        def is_number(token):
            if isinstance(token, int | float):
                return True
            elif isinstance(token, NoneType):
                return False
            else:
                result = True
                for s in token:
                    if s in '1234567890.,':  # garbage
                        continue
                    else:
                        result = False
                        break
                return result

        with sqlite3.connect(":memory:") as sqlite_connection:
            sqlite_connection.create_function("is_number", 1, is_number)
            cursor = sqlite_connection.cursor()
            cursor.executescript(calc_string)
            data_result = cursor.execute(select_string).fetchone()

        bar = datetime.datetime.now()
        data_result = dict((name.replace('"', ''), value) for name, value in
                           zip(list(data_result)[0::2], list(data_result)[1::2]))
        print(data_result)
        print(bar - foo)
        return data_result


class SqliteConnectionDB(Connection):

    def calculator(self, calc_string, select_string) -> dict:
        foo = datetime.datetime.now()

        sqlite_connection = sqlite3.connect("formula_commit.db")
        cursor = sqlite_connection.cursor()
        cursor.executescript('drop table test' + calc_string)
        p = cursor.execute(select_string).fetchall()

        bar = datetime.datetime.now()
        p = dict(p)
        print(p)
        print(bar - foo)
        return p


class SqliteConnectionUsingMemoryFactory(AbstractConnectionFactory):

    def connect(self) -> Connection:
        return SqliteConnectionMemory()


class SqliteConnectionDBFactory(AbstractConnectionFactory):

    def connect(self) -> Connection:
        return SqliteConnectionDB()
