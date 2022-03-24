import datetime
import unittest

from memory_profiler import profile

from FormulaCommit import IntegerField, StringField, FormulaCalculation, CalculationFactorySqlite, BoolField


class CheckResultGost_17_2_4_06Test(unittest.TestCase):

    @profile(precision=4)
    def test_ResultFind_gost_2477_2014(self):
        data = [IntegerField(symbol="@densityAir", formula="1.293", value="1.293", round_to=-3, definition_number="1",
                             primary_key="1"),
                IntegerField(symbol="@absHumidity", round_to=-1, value="1.6", definition_number="1", primary_key="2"),
                IntegerField(symbol="@tGas", round_to=-2, value="15.3", definition_number="1", primary_key="3"),
                IntegerField(symbol="@pAtmo", round_to=-2, value="98.8", definition_number="1", primary_key="4"),
                IntegerField(symbol="@Pd", round_to=-2, value="228.16", definition_number="1", primary_key="5"),
                IntegerField(symbol="@pStat", round_to=-2, value="813.61", definition_number="1", primary_key="6"),
                IntegerField(symbol="@exp", round_to=-2, formula="SQRT(2*@Pd/@densityWork)", value="",
                             definition_number="1", primary_key="7"),
                IntegerField(symbol="@concentrationWater", round_to=-5,
                             formula="round(((@densityAir*@absHumidity)/1000),5)", value="0.00207",
                             definition_number="1", primary_key="8"),
                IntegerField(symbol="@densityGas", round_to=-5,
                             formula="round((@densityAir+@concentrationWater)/(1+1.244*@concentrationWater),3)",
                             value="1.292", definition_number="1", primary_key="9"),
                IntegerField(symbol="@densityWork", round_to=-3,
                             formula="round((2.695*@densityGas*(@pAtmo+@pStat/1000)/(273+@tGas)),3)", value="1.203",
                             definition_number="1", primary_key="10"),
                StringField(symbol="@X", formula="avg(@exp)", value="19.48", primary_key="11")
                ]
        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print('Функция целиком: ', bar - foo)
        assert result == {'1': 1.293, '2': 1.6, '3': 15.3, '4': 98.8, '5': 228.16, '6': 813.61, '7': 19.48,
                          '8': 0.00207,
                          '9': 1.292, '10': 1.203, '11': '19.48'}, \
            "Неверное решение ГОСТ 17.2.4.06-90"

    @profile(precision=4)
    def test_ResultFind_gost_17_2_4_06_v2(self):
        data = [IntegerField(symbol="@v", formula="", value=20.25, round_to=-2, definition_number="1",
                             primary_key="1"),
                IntegerField(symbol="@pStat", round_to=-2, value=-1008, definition_number="1", primary_key="2"),
                IntegerField(symbol="@pAtmo", round_to=-2, value=98.9, definition_number="1", primary_key="3"),
                IntegerField(symbol="@tGas", round_to=-2, value=19.1, definition_number="1", primary_key="4"),
                StringField(symbol="@sRectangle", round_to=-4,
                            formula="(case when @flueLength>0 then REPLACE (round(CAST(@flueLength*@width/1000000 as DECIMAL(15,4)),4),'.',',') else REPLACE ('-','.',',')end)",
                            value="-", definition_number="1", primary_key="5"),
                IntegerField(symbol="@flueLength", round_to=-2,
                             formula="", value="", definition_number="1", primary_key="6"),
                StringField(symbol="@sRound", round_to=-4,
                            formula="(case when @diameter>0 then REPLACE(round(CAST((3.14*(@diameter*@diameter))/(4000000)as DECIMAL(15,4)),4),'.',',')else REPLACE ('-','.',',')end)",
                            value="0.1590", definition_number="1", primary_key="7"),
                IntegerField(symbol="@x2", round_to=-5,
                             formula="round(2.695*@x*(@pAtmo+@pStat/1000)/(273+@tGas),3)",
                             value=2.908, definition_number="1", primary_key="8"),
                BoolField(symbol="@input_manual", value="True", definition_number="1", primary_key="18"),
                StringField(symbol="@x", round_to=-5,
                            formula="(case when @sRectangle>0 then REPLACE (round((@v*@sRectangle),3),'.',',')else REPLACE (round((@v*@sRound),3),'.',',')end)",
                            value="3.220", definition_number="1", primary_key="9"),
                IntegerField(symbol="@d", formula="", value=470, round_to=-2, definition_number="1",
                             primary_key="10"),
                StringField(symbol="@diameter",
                            formula="(case when @d>0 then REPLACE (@d-@h,'.',',')else REPLACE ('-','.',',')end)",
                            value="450", round_to=-2, definition_number="1",
                            primary_key="11"),
                IntegerField(symbol="@width", formula="", value="", round_to=-2, definition_number="1",
                             primary_key="12"),
                IntegerField(symbol="@h", formula="", value=20, round_to=-2, definition_number="1",
                             primary_key="13"),

                StringField(symbol="@exp", formula="avg(@x)", value="", round_to=-3, round_with_zeros=True,
                            primary_key="14"),
                StringField(symbol="@abs_pogr", formula="max(@x)-min(@x)", round_to=-1, value="0,0",
                            primary_key="15"),
                StringField(symbol="@exp2", formula="avg(@x2)", value="", round_to=-3, primary_key="16"),
                StringField(symbol="@abs_pogr2", formula="max(@x2)-min(@x2)", round_to=-1, value="0,0",
                            primary_key="17"),

                ]
        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print('Функция целиком: ', bar - foo)
        print(result)
        assert result == {'1': 20.25, '2': -1008, '3': 98.9, '4': 19.1, '5': '-', '6': '', '7': '0.1590',
                          '8': 2.908, '18': True, '9': '3.220', '10': 470.0, '11': '450', '12': '', '13': 20.0,
                          '14': '3.220', '15': '0.0', '16': '', '17': ''}, \
            "Неверное решение ГОСТ 17.2.4.06-90"


class CheckResultTest(unittest.TestCase):

    @profile(precision=4)
    def test_ResultFind_simple_sum(self):
        data = [IntegerField(symbol="@a", formula="", value="2", primary_key=1),
                IntegerField(symbol="@b", formula="", value="6", primary_key=2),
                IntegerField(symbol="@c", formula="@a+@b", value="2", primary_key=3)]
        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print('Функция целиком: ', bar - foo)
        assert result == {1: 2.0, 2: 6.0, 3: 8.0}, "Неверное решение simple_sum"

    @profile(precision=4)
    def test_ResultFind_sum_lower_number(self):
        data = [IntegerField(symbol="@a", value=19.476097420679974123, round_to='-', primary_key=1),
                IntegerField(symbol="@b", value=6, primary_key=2),
                IntegerField(symbol="@c", formula="@a+@b", round_to='-', value=2, primary_key=3)]
        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print(result)
        print('Функция целиком: ', bar - foo)
        assert result == {1: 19.476097420679974, 2: 6.0, 3: 25.476097420679974}, "Неверное решение lower_number"


class CheckResultGost_2477_2014Test(unittest.TestCase):

    @profile(precision=4)
    def test_ResultFind_gost_2477_2014(self):
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
        assert result == {'1': '2', '2': 'Да', '3': '1', '4': '1', '5': True, '6': False, '7': '', '8': 1.0,
                          '9': 1.0, '10': False, '11': False, '12': 100.0, '13': 100.0, '14': '100.0'}, \
            "Неверное решение Гост 2477-2014"

    @profile(precision=4)
    def test_ResultFind_gost_2477_2014_all_check(self):
        data = [StringField(symbol="", formula="", value="2", primary_key="1"),
                StringField(symbol="", formula="", value="Да", primary_key="2"),

                IntegerField(symbol="@V0", formula="", value="1", definition_number="1", primary_key="3"),
                IntegerField(symbol="@m", formula="", value="1", definition_number="1", primary_key="4"),
                BoolField(symbol="@check_ignore", value="True", definition_number="1", primary_key="5"),
                BoolField(symbol="@input_manual", value="False", definition_number="1", primary_key="6"),
                IntegerField(symbol="@exp", formula="(@V0/@m)*100", value="7", definition_number="1", primary_key="7"),
                IntegerField(symbol="@V0", formula="", value="1", definition_number="2", primary_key="8"),
                IntegerField(symbol="@m", formula="", value="1", definition_number="2", primary_key="9"),
                BoolField(symbol="@check_ignore", value="True", definition_number="2", primary_key="10"),
                BoolField(symbol="@input_manual", value="False", definition_number="2", primary_key="11"),
                IntegerField(symbol="@exp", formula="(@V0/@m)*100", value="8", definition_number="2", primary_key="12"),

                IntegerField(symbol="@av", formula="avg(@exp)", value="", primary_key="13"),

                StringField(symbol="@r", formula="avg(@exp)", value="", primary_key="14")]
        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print('Функция целиком: ', bar - foo)
        assert result == {'1': '2', '2': 'Да', '3': '1', '4': '1', '5': True, '6': False, '7': '7', '8': '1',
                          '9': '1', '10': True, '11': False, '12': '8', '13': '', '14': ''}, \
            "Неверное решение Гост 2477-2014"


class CheckFormulaIFResultTest(unittest.TestCase):

    @profile(precision=4)
    def test_Sqlite_IF1_v1(self):
        data = [StringField(symbol="@t", formula="", value="Привет", definition_number="1", primary_key="1"),
                StringField(symbol="@t", formula="", value="Привет", definition_number="2", primary_key="2"),
                StringField(symbol="@exp", formula='if(@t_1 = 1, 1,  if (@t_1 = 2, 2 , "Enother"))', value="500",
                            definition_number="1", primary_key="3")
                ]
        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print('Функция целиком: ', bar - foo)
        assert result == {'1': 'Привет', '2': 'Привет', '3': 'Enother'}, \
            "Неверное решение ResultOnly 1 param"

    @profile(precision=4)
    def test_Sqlite_IF1_v2(self):
        data = [StringField(symbol="@t", formula="", value="Привет1", definition_number="1", primary_key="1"),
                StringField(symbol="@t", formula="", value="Привет", definition_number="2", primary_key="2"),
                StringField(symbol="@exp", formula='if(@t_1 = "Привет1", "1",  if (@t_1 = 2, 2 , "Enother"))',
                            value="500", definition_number="1", primary_key="3")
                ]
        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print('Функция целиком: ', bar - foo)
        assert result == {'1': 'Привет1', '2': 'Привет', '3': '1'}, \
            "Неверное решение ResultOnly 1 param"

    @profile(precision=4)
    def test_Sqlite_IF2_v1(self):
        data = [StringField(symbol="@t", formula="", value="Привет", definition_number="1", primary_key="1"),
                StringField(symbol="@t", formula="", value="Привет", definition_number="2", primary_key="2"),
                StringField(symbol="@exp", formula='if    (@t_1 = 1, 1, "Enother")', value="500",
                            definition_number="1", primary_key="3")
                ]
        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print('Функция целиком: ', bar - foo)
        assert result == {'1': 'Привет', '2': 'Привет', '3': 'Enother'}, \
            "Неверное решение ResultOnly 1 param"

    @profile(precision=4)
    def test_Sqlite_IF2_v2(self):
        data = [StringField(symbol="@t", formula="", value="Привет", definition_number="1", primary_key="1"),
                StringField(symbol="@t", formula="", value="Привет", definition_number="2", primary_key="2"),
                StringField(symbol="@exp", formula='if    (@t_1 = "Привет", "1", "Enother")', value="500",
                            definition_number="1", primary_key="3")
                ]
        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print('Функция целиком: ', bar - foo)
        assert result == {'1': 'Привет', '2': 'Привет', '3': '1'}, \
            "Неверное решение ResultOnly 1 param"

    @profile(precision=4)
    def test_Sqlite_IF_ResultOnly_v1(self):
        data = [StringField(symbol="@t", formula="", value="Привет", definition_number="1", primary_key="1"),
                StringField(symbol="@t", formula="", value="Привет", definition_number="2", primary_key="2"),
                StringField(symbol="@exp", formula='if(only(@t, "Разногласие по параметрам") = "Привет",'
                                                   ' "1", "Enother")', value="500",
                            definition_number="1", primary_key="3")
                ]
        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print('Функция целиком: ', bar - foo)
        assert result == {'1': 'Привет', '2': 'Привет', '3': '1'}, \
            "Неверное решение ResultOnly 1 param"

    @profile(precision=4)
    def test_Sqlite_IF2_v3(self):
        data = [StringField(symbol="@t", value=0.001, primary_key="1"),
                StringField(symbol="@z", formula="if(cast(sum(@t) as char) = @t, 1, 0)", primary_key="2")]

        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print(result)
        print('Функция целиком: ', bar - foo)
        assert result == {'1': '0.001', '2': '1'}, \
            "Неверное решение RoundWithZero"

    @profile(precision=4)
    def test_Sqlite_IF2_v4(self):
        data = [IntegerField(symbol="@t", value=1, definition_number="1", primary_key="1"),
                IntegerField(symbol="@t", value=2, definition_number="2", primary_key="2"),
                StringField(symbol="@exp", formula='if (@t = max (@t), 1, 0 )', value="500",
                            definition_number="1", primary_key="3"),
                StringField(symbol="@exp", formula='if (@t = max (@t), 1, 0 )', value="500",
                            definition_number="2", primary_key="4")
                ]
        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print('Функция целиком: ', bar - foo)
        assert result == {'1': 1.0, '2': 2.0, '3': '0', '4': '1'}, \
            "Неверное решение ResultOnly 1 param"


class CheckFormulaOnlyResultTest(unittest.TestCase):

    @profile(precision=4)
    def test_1param_equals(self):
        data = [StringField(symbol="@t", formula="", value="Привет", definition_number="1", primary_key="1"),
                StringField(symbol="@t", formula="", value="Привет", definition_number="2", primary_key="2"),
                StringField(symbol="@exp", formula='only(@t, "Разногласие по параметрам")', value="500",
                            definition_number="1", primary_key="3")
                ]
        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print('Функция целиком: ', bar - foo)
        assert result == {'1': 'Привет', '2': 'Привет', '3': 'Привет'}, \
            "Неверное решение ResultOnly 1 param"

    @profile(precision=4)
    def test_1param_not_equals(self):
        data = [StringField(symbol="@t", formula="", value="Привет", definition_number="1", primary_key="1"),
                StringField(symbol="@t", formula="", value="Привет1", definition_number="2", primary_key="2"),
                StringField(symbol="@exp", formula='only(@t, "Разногласие по параметрам")', value="500",
                            definition_number="1", primary_key="3")
                ]
        foo = datetime.datetime.now()
        result = FormulaCalculation(data, CalculationFactorySqlite()).calc()
        bar = datetime.datetime.now()
        print('Функция целиком: ', bar - foo)
        assert result == {'1': 'Привет', '2': 'Привет1', '3': 'Разногласие по параметрам'}, \
            "Неверное решение ResultOnly 1 param"
