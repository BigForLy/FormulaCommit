from sqlalchemy.future import create_engine
from sqlalchemy.orm import sessionmaker

from FormulaCommit.fields import StringField, IntegerField, BoolField
from FormulaCommit.manage import FormulaManagerMySql


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


session = test_connection()
# p = z.execute(text("select @z := 1 + 2 as z"))
# p = p.all()


data = [IntegerField(symbol="", formula="", value="2"),  # все не блокируемые поля имеют номер определения 0
        IntegerField(symbol="", formula="1+2", value="200"),
        IntegerField(symbol="@t", formula="", value="2", definition_number="1"),
        IntegerField(symbol="@t1", formula="", value="1", definition_number="1"),
        IntegerField(symbol="@h", formula="", value="1", definition_number="1"),
        BoolField(symbol="@check_ignore", value="False", definition_number="1"),
        BoolField(symbol="@input_manual", value="False", definition_number="1"),
        IntegerField(symbol="@exp", formula="@t+0.00016*(@t-@t1)*@h", value="500", definition_number="1"),
        IntegerField(symbol="@t", formula="", value="3", definition_number="2"),
        IntegerField(symbol="@t1", formula="", value="1", definition_number="2"),
        IntegerField(symbol="@h", formula="", value="1", definition_number="2"),
        BoolField(symbol="@check_ignore", value="False", definition_number="2"),
        BoolField(symbol="@input_manual", value="False", definition_number="2"),
        IntegerField(symbol="@exp", formula="@t+0.00016*(@t-@t1)*@h", value="50", definition_number="2"),
        IntegerField(symbol="@r1",
                     formula="/*смисмисм*/REPLACE((case when avg(@exp)=1 then '1,00' when avg(@exp)=2 then '2,00' when avg(@exp)=3 then '3,00' when avg(@exp)=4 then '4,00' when avg(@exp)=5 then '5,0' else avg(@exp) end),',','.')"),
        IntegerField(symbol="@r2",
                     formula="avg(@exp)+1")
        ]

import datetime

foo = datetime.datetime.now()
a = FormulaManagerMySql(data, session).calc()
bar = datetime.datetime.now()
print(dict(map(lambda x: (x.symbol_item.symbol_and_definition, x.value), a)))
print('Функция целиком: ', bar - foo)

# data_formula1 = {"@t_1": StringField(symbol="@t", formula="", value="Привет", opred_number="1"),
#                  "@t_2": StringField(symbol="@t", formula="", value="Привет", opred_number="2"),
#                  "@exp_1": StringField(symbol="@exp", formula='only(@t, "Разногласие по параметрам")', value="500",
#                                        opred_number="1")
#                  }
