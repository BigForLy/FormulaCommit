from sqlalchemy.future import create_engine
from sqlalchemy.orm import sessionmaker

from FormulaCommit.fields import StringField, IntegerField
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


data_formula2 = {"@t_1": IntegerField(symbol="@t", formula="", value="2", opred_number="1"),
                 "@t1_1": IntegerField(symbol="@t1", formula="", value="1", opred_number="1"),
                 "@h_1": IntegerField(symbol="@h", formula="", value="1", opred_number="1"),
                 "@exp_1": IntegerField(symbol="@exp", formula="@t+0.00016*(@t-@t1)*@h", value="500",
                                        opred_number="1", value_only=True),
                 "@t_3": IntegerField(symbol="@t", formula="", value="3", opred_number="3"),
                 "@t1_3": IntegerField(symbol="@t1", formula="", value="1", opred_number="3"),
                 "@h_3": IntegerField(symbol="@h", formula="", value="1", opred_number="3"),
                 "@exp_3": IntegerField(symbol="@exp", formula="@t+0.00016*(@t-@t1)*@h", opred_number="3"),
                 "@r1_1": IntegerField(symbol="@r1", formula="/*смисмисм*/REPLACE((case when avg(@exp)=1 then '1,00' when avg(@exp)=2 then '2,00' when avg(@exp)=3 then '3,00' when avg(@exp)=4 then '4,00' when avg(@exp)=5 then '5,0' else avg(@exp) end),',','.')")
                 }


data_formula1 = {"@t_1": StringField(symbol="@t", formula="", value="Привет", opred_number="1"),
                 "@t_2": StringField(symbol="@t", formula="", value="Привет", opred_number="2"),
                 "@exp_1": StringField(symbol="@exp", formula='only(@t, "Разногласие по параметрам")', value="500",
                                       opred_number="1")
                 }

import datetime

print(datetime.datetime.now())
opred = 2
a = FormulaManagerMySql(data_formula2, session, opred).calc()
print(a)
print(datetime.datetime.now())

data_new = {"@d": IntegerField(symbol="@d", formula="@a**@c"),
            "@ab": IntegerField(symbol="@ab", formula="@d+@c"),
            "@e": IntegerField(symbol="@e", formula="round(@z, 1)"),
            "@z": IntegerField(symbol="@z", formula="@a+@ab + 1"),
            "@a": IntegerField(symbol="@a", formula="5.4"),
            "@b": IntegerField(symbol="@b", formula="10"),
            "@c": IntegerField(symbol="@c", formula="@a+@b")}  # "a+b", {"a":5.4, "b":10}

# print(datetime.datetime.now())
# a = FormulaManagerPython(data_new).calc()
# print(a)
# print(datetime.datetime.now())
