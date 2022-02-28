from sqlalchemy import text, literal_column, literal
from sqlalchemy.future import create_engine
from sqlalchemy.orm import sessionmaker

from FormulaCommit.fields import StringField, IntegerField
from FormulaCommit.manage import FormulaManagerMySql, FormulaManagerPython


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

# Гост 18995.4-73
data_formula2 = {"@t_1": IntegerField(symbol="@t_1", formula="", value="2", opred_number="1"),
                 "@t1_1": IntegerField(symbol="@t1_1", formula="", value="1", opred_number="1"),
                 "@h_1": IntegerField(symbol="@h_1", formula="", value="1", opred_number="1"),
                 "@exp_1": IntegerField(symbol="@exp_1", formula="@t+0.00016*(@t-@t1)*@h", value="500",
                                        opred_number="1"),
                 "@t_2": IntegerField(symbol="@t_2", formula="", value="3", opred_number="2"),
                 "@t1_2": IntegerField(symbol="@t1_2", formula="", value="1", opred_number="2"),
                 "@h_2": IntegerField(symbol="@h_2", formula="", value="1", opred_number="2"),
                 "@exp_2": IntegerField(symbol="@exp_2", formula="@t+0.00016*(@t-@t1)*@h", opred_number="2"),
                 "@r1": IntegerField(symbol="@r1", formula="5+avg(@exp)")
                 }

data_formula1 = {"@t_1": StringField(symbol="@t", formula="", value="Привет", opred_number="1"),
                 "@t_2": StringField(symbol="@t", formula="", value="Привет", opred_number="2"),
                 "@exp": StringField(symbol="@exp", formula="only(@t, \'Разногласие по параметрам\', \'Не разногласие\')", value="500",
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
            # "@e": IntegerField(symbol="@e", formula="round(@z, int(1))"),
            "@e": IntegerField(symbol="@e", formula="round(@z, 1)"),
            "@z": IntegerField(symbol="@z", formula="@a+@ab + 1"),
            "@a": IntegerField(symbol="@a", formula="5.4"),
            "@b": IntegerField(symbol="@b", formula="10"),
            "@c": IntegerField(symbol="@c", formula="@a+@b")}  # "a+b", {"a":5.4, "b":10}

# print(datetime.datetime.now())
# a = FormulaManagerPython(data_new).calc()
# print(a)
# print(datetime.datetime.now())
