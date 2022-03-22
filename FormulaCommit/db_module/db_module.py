# https://qna.habr.com/q/1066566
# https://coderlessons.com/tutorials/bazy-dannykh/vyuchit-sqlite/sqlite-kratkoe-rukovodstvo
from abc import ABC, abstractmethod


class Connection(ABC):
    @abstractmethod
    def calculator(self, calc_string, select_string) -> dict:
        pass


class AbstractConnectionFactory(ABC):

    @abstractmethod
    def connect(self) -> Connection:
        pass
