from FormulaCommit.formula_mysql import FormulaAvg

OPERATORS = {'+': (1, lambda x, y: x + y), '-': (1, lambda x, y: x - y),
             '*': (2, lambda x, y: x * y), '/': (2, lambda x, y: x / y)}

FUNC = {'avg': FormulaAvg()}  # кол-во аргументов, делимитр аргументов, функция


def parse(formula_string):
    param = ''
    for s in formula_string:
        if s in OPERATORS or s in "( ,)":  # garbage
            if param:
                yield param
            yield s
            param = ''
        else:
            param += s
    if param:
        yield param


def shunting_yard(parsed_formula):
    stack = []
    for token in parsed_formula:
        if token in FUNC:
            while stack and stack[-1] != "(":
                yield stack.pop()
            stack.append(token)
        elif token == ")":
            s = []
            while stack:
                x = stack.pop()
                if x == "(":
                    break
                s.append(x)
            stack.append(''.join(s[::-1]))
        elif token == "(":
            stack.append(token)
        else:
            stack.append(token)
    stack = stack[::-1]
    while stack:
        x = stack.pop()
        if x in FUNC:
            param = []
            current_func = FUNC[x]
            for i in range(current_func.count_param):
                param.append(stack.pop())
            yield current_func.get_transformation(param)
        else:
            yield x


# print(list(parse('@t+1')))
# print(list(shunting_yard(parse('@t+1'))))
# print(list(parse('avg(@t_1+1)+5')))
# print(list(shunting_yard(parse('(1*3)+avg(@t_1+1)+5'))))
# print(list(shunting_yard(parse('(1*3)+5*avg(@t_1+1)+5'))))

# print(list(shunting_yard(parse('(1*3)+5*avg((@t_1+1)*5)+5'))))
print(list(shunting_yard(parse('avg(5, "Ghbd tn")'))))
# print(list(shunting_yard(parse('avg(@t)+5'))))

