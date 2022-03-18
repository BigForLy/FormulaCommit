import datetime
import sqlite3
# https://qna.habr.com/q/1066566
# https://coderlessons.com/tutorials/bazy-dannykh/vyuchit-sqlite/sqlite-kratkoe-rukovodstvo
from abc import ABC, abstractmethod
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


# function StrToFloatLocalTrue(const s: string): Boolean;
# var
#   stringS: string;
# begin
#   stringS := StringReplace(s, '.', string(FormatSettings.DecimalSeparator), []);
#   stringS := StringReplace(stringS, ',', string(FormatSettings.DecimalSeparator), []);
#   result:=(StrToFloatDef(stringS, -123700.321007) <> -123700.321007);
# end;


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


class Connection(ABC):
    @abstractmethod
    def calculator(self, calc_string, select_string) -> dict:
        pass


class MySQLConnection(Connection):

    def calculator(self, calc_string, select_string) -> dict:
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


class SqliteConnectionMemory(Connection):

    def calculator(self, calc_string, select_string) -> dict:
        foo = datetime.datetime.now()

        with sqlite3.connect(":memory:") as sqlite_connection:
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


class AbstractConnectionFactory(ABC):

    @abstractmethod
    def connect(self) -> Connection:
        pass


class MySQLConnectionFactory(AbstractConnectionFactory):

    def connect(self) -> Connection:
        return MySQLConnection()


class SqliteConnectionUsingMemoryFactory(AbstractConnectionFactory):

    def connect(self) -> Connection:
        return SqliteConnectionMemory()


class SqliteConnectionDBFactory(AbstractConnectionFactory):

    def connect(self) -> Connection:
        return SqliteConnectionDB()



