from sqlalchemy import text, literal_column, literal
from sqlalchemy.future import create_engine
from sqlalchemy.orm import sessionmaker

from FormulaCommit.fields import StringField, IntegerField
from FormulaCommit.manage import FormulaManager


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


z = test_connection()
# p = z.execute(text("select @z := 1 + 2 as z"))
# p = p.all()


data = {"@d": "@a**@c",
        "@ab": "@d+@c",
        "@e": "round(@z, int(1))",
        "@z": "@a+@ab + 1",
        "@a": "5.4",
        "@b": "10",
        "@c": "@a+@b"}

data_formula2 = {"@z": IntegerField(symbol="@z", formula="1+2"),
                "@d": IntegerField(symbol="@d", formula="CASE WHEN @z >4 THEN 2 WHEN @z <=3 THEN 1 END"),
                "@p_1": IntegerField(symbol="@p_1", formula="1+2"),
                "@p_2": IntegerField(symbol="@p_2", formula="1+2")}

data_new = {"@d": IntegerField(symbol="@d", formula="@a**@c"),
            "@ab": IntegerField(symbol="@ab", formula="@d+@c"),
            # "@e": IntegerField(symbol="@e", formula="round(@z, int(1))"),
            "@e": IntegerField(symbol="@e", formula="@z"),
            "@z": IntegerField(symbol="@z", formula="@a+@ab + 1"),
            "@a": IntegerField(symbol="@a", formula="5.4"),
            "@b": IntegerField(symbol="@b", formula="10"),
            "@c": IntegerField(symbol="@c", formula="@a+@b")}


data_formula = {"@exp": IntegerField(symbol="@exp", formula="2"),
                "@exp_1": IntegerField(symbol="@exp_1", formula="2"),
                "@exp_2": IntegerField(symbol="@exp_2", formula="3"),
                "@result_1": IntegerField(symbol="@result_1", formula="avg(@exp)")}


import datetime
print(datetime.datetime.now())

if method_type=2:
    a = FormulaManager(data_formula2).calc_mysql(z)
else:
    a = FormulaManager(data_formula2).calc_python()
print(a)
print(datetime.datetime.now())
# FormulaManager(data_new).calc()
