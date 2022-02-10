from FormulaCommit.fields import StringField, IntegerField
from FormulaCommit.manage import FormulaManager

data = {"@d": "@a**@c",
        "@ab": "@d+@c",
        "@e": "round(@z, int(1))",
        "@z": "@a+@ab + 1",
        "@a": "5.4",
        "@b": "10",
        "@c": "@a+@b"}

data_new = {"@d": IntegerField(symbol="@d", formula="@a**@c"),
            "@ab": IntegerField(symbol="@ab", formula="@d+@c"),
            "@e": IntegerField(symbol="@e", formula="round(@z, int(1))"),
            "@z": IntegerField(symbol="@z", formula="@a+@ab + 1"),
            "@a": IntegerField(symbol="@a", formula="5.4"),
            "@b": IntegerField(symbol="@b", formula="10"),
            "@c": IntegerField(symbol="@c", formula="@a+@b")}

FormulaManager(data_new).calc()
