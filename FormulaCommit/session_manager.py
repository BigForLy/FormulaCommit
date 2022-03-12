import datetime
import sqlite3
# https://qna.habr.com/q/1066566
from abc import ABC, abstractmethod

from memory_profiler import memory_usage
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# foo = datetime.datetime.now()
# sqlite_connection = sqlite3.connect(":memory:")
#
# cursor = sqlite_connection.cursor()
#
# cursor.executescript("""
#     create table test(name, value);
#     insert into test(name, value) values ("@a_1", 3),  ("@a_2", 2);
#     insert into test(name, value) values ("@a_3",
#                 (select avg(value) from test where name = "@a_1" or name = "@a_2")
#                                          );
#     """)
# p = cursor.execute('select * from test').fetchall()
# bar = datetime.datetime.now()
# print(p)
# print(dict(p))
# print(bar - foo)
from FormulaCommit.parse_sql import CalculateItem


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
        const_item_formula = []
        calc_item_formula = []
        for item in symbol_and_calculate_item_list:
            if item.is_formula:
                calc_item_formula.append(f'insert into test(name, value) value ({item.formula});')
            else:
                const_item_formula.append(item.formula)
        calc_string = 'create table test(name, value); insert into test(name, value) values ' \
                      f'{" ".join(const_item_formula)}; {" ".join(calc_item_formula)}'
        select_string = ' select ' + ', '.join(list(map(lambda x: x[1].symbol_and_definition,
                                                        symbol_and_calculate_item_list))) + 'from test'
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


class Calculator(ABC):
    @abstractmethod
    def calculation(self, calc_string, select_string) -> dict:
        pass


class MySQLCalculator(Calculator):

    def __init__(self, parser):
        self.__parser = parser

    def calculation(self, calc_string, select_string) -> dict:
        def test_connection():
            db = "mysql://root:3kmzghj3z@localhost:3306/lims?charset=utf8"
            engine = create_engine(
                db,
                pool_recycle=3600,
                connect_args={
                    'connect_timeout': 1
                }
            )
            session = sessionmaker(bind=engine)
            return session()

        foo = datetime.datetime.now()

        session = test_connection()
        session.execute(text(calc_string))
        dataset = session.execute(text(select_string)).all()

        bar = datetime.datetime.now()
        print('Запрос к базе:   ', bar - foo)
        print(dataset[0]._mapping)
        return dataset[0]._mapping


class SqliteCalculatorMemory(Calculator):

    def __init__(self, parser):
        self.__parser = parser

    def calculation(self, calc_string, select_string)-> dict:
        foo = datetime.datetime.now()

        sqlite_connection = sqlite3.connect(":memory:")
        cursor = sqlite_connection.cursor()
        cursor.executescript(calc_string)
        p = cursor.execute(select_string).fetchall()

        bar = datetime.datetime.now()
        p = dict(p)
        print(p)
        print(bar - foo)
        return p


class SqliteCalculatorDB(Calculator):

    def __init__(self, parser):
        self.__parser = parser

    def calculation(self, calc_string, select_string) -> dict:
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


class AbstractCalculationPlatformFactory(ABC):
    @abstractmethod
    def calculator(self) -> Calculator:
        pass


class MySQLFactory(AbstractCalculationPlatformFactory):

    def calculator(self) -> Calculator:
        return MySQLCalculator(ParserCalculationItemToExecuteStringMySQL())


class SqliteMemoryFactory(AbstractCalculationPlatformFactory):

    def calculator(self) -> Calculator:
        return SqliteCalculatorMemory(ParserCalculationItemToExecuteStringSqlite())


class SqliteDBFactory(AbstractCalculationPlatformFactory):

    def calculator(self) -> Calculator:
        return SqliteCalculatorDB(ParserCalculationItemToExecuteStringSqlite())


# print(memory_usage())
