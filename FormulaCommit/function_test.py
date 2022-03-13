import datetime
from unittest import TestCase
from memory_profiler import profile
from FormulaCommit.fields import IntegerField, StringField, BoolField
from FormulaCommit.manage import FormulaCalculation, CalculationFactoryMySql, CalculationFactorySqlite


class CheckResultTest(TestCase):

    @profile(precision=4)
    def test_ResultFind_simple_sum(self):
        data = [IntegerField(symbol="@a", formula="", value="2", primary_key=1),
                IntegerField(symbol="@b", formula="", value="6", primary_key=2),
                IntegerField(symbol="@c", formula="@a+@b", value="2", primary_key=3)]
        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactoryMySql()).calc()
        bar = datetime.datetime.now()
        print('Функция целиком: ', bar - foo)
        assert result == {1: 2.0, 2: 6.0, 3: 8.0}, "Неверное решение simple_sum MySQL"

    @profile(precision=4)
    def test_ResultFind_MySQL_gost_2477_2014(self):
        data = [StringField(symbol="", formula="", value="2", primary_key="1"),
                StringField(symbol="", formula="", value="Да", primary_key="2"),

                IntegerField(symbol="@V0", formula="", value="1", definition_number="1", primary_key="3"),
                IntegerField(symbol="@m", formula="", value="1", definition_number="1", primary_key="4"),
                BoolField(symbol="@check_ignore", value="True", definition_number="1", primary_key="5"),
                BoolField(symbol="@input_manual", value="False", definition_number="1", primary_key="6"),
                IntegerField(symbol="@exp", formula="(@V0/@m)*100", value="", definition_number="1", primary_key="7"),
                IntegerField(symbol="@V0", formula="", value="1", definition_number="2", primary_key="8"),
                IntegerField(symbol="@m", formula="", value="1", definition_number="2", primary_key="9"),
                BoolField(symbol="@check_ignore", value="False", definition_number="2", primary_key="10"),
                BoolField(symbol="@input_manual", value="False", definition_number="2", primary_key="11"),
                IntegerField(symbol="@exp", formula="(@V0/@m)*100", value="", definition_number="2", primary_key="12"),

                IntegerField(symbol="@av", formula="avg(@exp)", value="", primary_key="13"),

                StringField(symbol="@r", formula="avg(@exp)", value="", primary_key="14")]
        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactoryMySql()).calc()
        bar = datetime.datetime.now()
        print('Функция целиком: ', bar - foo)
        assert result == {'1': '2', '2': 'Да', '13': 100.0, '14': 100.0, '3': 1.0, '4': 1.0, '5': True,
                          '6': False, '7': '', '8': 1.0, '9': 1.0, '10': 'False', '11': 'False', '12': 100.0}, \
            "Неверное решение Гост 2477-2014 MySql"

    @profile(precision=4)
    def test_ResultFind_Sqlite_gost_2477_2014(self):
        data = [StringField(symbol="", formula="", value="2", primary_key="1"),
                StringField(symbol="", formula="", value="Да", primary_key="2"),

                IntegerField(symbol="@V0", formula="", value="1", definition_number="1", primary_key="3"),
                IntegerField(symbol="@m", formula="", value="1", definition_number="1", primary_key="4"),
                BoolField(symbol="@check_ignore", value="True", definition_number="1", primary_key="5"),
                BoolField(symbol="@input_manual", value="False", definition_number="1", primary_key="6"),
                IntegerField(symbol="@exp", formula="(@V0/@m)*100", value="", definition_number="1", primary_key="7"),
                IntegerField(symbol="@V0", formula="", value="1", definition_number="2", primary_key="8"),
                IntegerField(symbol="@m", formula="", value="1", definition_number="2", primary_key="9"),
                BoolField(symbol="@check_ignore", value="False", definition_number="2", primary_key="10"),
                BoolField(symbol="@input_manual", value="False", definition_number="2", primary_key="11"),
                IntegerField(symbol="@exp", formula="(@V0/@m)*100", value="", definition_number="2", primary_key="12"),

                IntegerField(symbol="@av", formula="avg(@exp)", value="", primary_key="13"),

                StringField(symbol="@r", formula="avg(@exp)", value="", primary_key="14")]
        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print('Функция целиком: ', bar - foo)
        assert result == {'1': '2', '2': 'Да', '13': 100.0, '14': 100.0, '3': 1.0, '4': 1.0, '5': True,
                          '6': False, '7': '', '8': 1.0, '9': 1.0, '10': 'False', '11': 'False', '12': 100.0}, \
            "Неверное решение Гост 2477-2014 Sqlite"
