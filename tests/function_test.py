import datetime
import unittest
from memory_profiler import profile
from FormulaCommit import *


class CheckFormula10ToDegreeTest(unittest.TestCase):

    @profile(precision=4)
    def test_Sqlite_ten_to_degree_v1(self):
        data = [StringField(symbol="@t", value=0.001000,
                            primary_key="1", ten_to_degree=True)]

        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print(result)
        print('Функция целиком: ', bar - foo)
        assert result == {'1': '1.0*10^-3'}, \
            "Неверное решение 10ToDegree Sqlite"

    @profile(precision=4)
    def test_Sqlite_ten_to_degree_v2(self):
        data = [StringField(symbol="@t", value=0.001001,
                            primary_key="1", ten_to_degree=True)]

        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print(result)
        print('Функция целиком: ', bar - foo)
        assert result == {'1': '1.001*10^-3'}, \
            "Неверное решение 10ToDegree Sqlite"

    @profile(precision=4)
    def test_Sqlite_ten_to_degree_v3(self):
        data = [StringField(symbol="@t", value=1001,
                            primary_key="1", ten_to_degree=True)]

        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print(result)
        print('Функция целиком: ', bar - foo)
        assert result == {'1': '1.001*10^3'}, \
            "Неверное решение 10ToDegree Sqlite"


class CheckFormulaRoundWithZeroTest(unittest.TestCase):

    @profile(precision=4)
    def test_Sqlite_round_with_zeros_v1(self):
        data = [StringField(symbol="@t", value=0.001, round_to=6, round_with_zeros=True,
                            primary_key="1")]

        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print(result)
        print('Функция целиком: ', bar - foo)
        assert result == {'1': '0.001000'}, \
            "Неверное решение RoundWithZero Sqlite"

    @profile(precision=4)
    def test_Sqlite_round_with_zeros_v2(self):
        data = [StringField(symbol="@t", value=0.1, round_to=6, round_with_zeros=True,
                            primary_key="1")]

        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print(result)
        print('Функция целиком: ', bar - foo)
        assert result == {'1': '0.100000'}, \
            "Неверное решение RoundWithZero Sqlite"

    @profile(precision=4)
    def test_Sqlite_round_with_zeros_v3(self):
        data = [StringField(symbol="@t", value=1, round_to=6, round_with_zeros=True,
                            primary_key="1")]

        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print(result)
        print('Функция целиком: ', bar - foo)
        assert result == {'1': '1'}, \
            "Неверное решение RoundWithZero Sqlite"


class CheckFormulaRoundToSignificantDigits(unittest.TestCase):

    @profile(precision=4)
    def test_Sqlite_round_to_significant_digits_v1(self):
        data = [StringField(symbol="@t", value=0.001000, round_to_significant_digits=True,
                            primary_key="1")]

        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print(result)
        print('Функция целиком: ', bar - foo)
        assert result == {'1': '0.001'}, \
            "Неверное решение RoundWithZero Sqlite"

    @profile(precision=4)
    def test_Sqlite_round_to_significant_digits_v2(self):
        data = [StringField(symbol="@t", value=0.000201, round_to_significant_digits=True,
                            primary_key="1")]

        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print(result)
        print('Функция целиком: ', bar - foo)
        assert result == {'1': '0.000201'}, \
            "Неверное решение RoundWithZero Sqlite"


class CheckFormulaRoundTo(unittest.TestCase):

    @profile(precision=4)
    def test_Sqlite_round_to_v1(self):
        data = [StringField(symbol="@t", value=0.0042, round_to_significant_digits=True, round_to=-3,
                            primary_key="1")]

        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print(result)
        print('Функция целиком: ', bar - foo)
        assert result == {'1': '0.004'}, \
            "Неверное решение RoundWithZero Sqlite"
