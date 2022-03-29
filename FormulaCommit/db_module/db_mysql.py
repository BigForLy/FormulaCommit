import datetime

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from FormulaCommit.db_module.db_module import Connection, AbstractConnectionFactory
from pathlib import Path
import os


class MySQLConnection(Connection):

    def calculator(self, calc_string, select_string) -> dict:
        def test_connection():
            load_dotenv()
            env_path = Path('.') / '.env'
            load_dotenv(dotenv_path=env_path)
            db = os.getenv("db")
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


class MySQLConnectionFactory(AbstractConnectionFactory):

    def connect(self) -> Connection:
        return MySQLConnection()
