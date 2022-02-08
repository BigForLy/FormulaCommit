import graphlib
import datetime

from FormulaCommit.parse import ParseManager

data = {"@d": "@a-@c",
        "@ab": "@d+@c",
        "@e": "round(@z, 0)",
        "@z": "@a+@ab",
        "@a": "5.4",
        "@b": "10",
        "@c": "@a+@b"}
print(datetime.datetime.now())
graph = {}

parse_manager = ParseManager()

for key, value in data.items():
    graph.update({key: set(parse_manager.parses(value))})

print(graph)

ts = graphlib.TopologicalSorter(graph)
z = tuple(ts.static_order())
print(z)

data2 = {}

for param in z:
    if param.find('@') == -1:  # число
        data2.update({param: float(param)})
    else:  # строка
        data2.update({param: float(eval(parse_manager.calc(data[param], data2)))})


print(data2)
print(datetime.datetime.now())
