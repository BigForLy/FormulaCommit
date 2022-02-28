import builtins

a = (1 if False else (2 if True else 3))
print(a)

a = 10.00

if int(a) == a:
    print(True)


def eee(p, b):
    return p + b


o = eval("eee(1, 2)")
print(o)


def round(p, b):
    return builtins.round(p, int(b))


o = eval("round(1, 2.0)")
print(o)

a = set()

a.update('q')


print(a)
