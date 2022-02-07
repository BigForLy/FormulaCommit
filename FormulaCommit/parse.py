OPERATORS = {'+': (1, lambda x, y: x + y), '-': (1, lambda x, y: x - y),
             '*': (2, lambda x, y: x * y), '/': (2, lambda x, y: x / y)}


def parse(formula_string):
    number = ''
    param = ''
    for s in formula_string:
        if s in '1234567890.':  # если символ - цифра, то  число
            number += s
        elif s in OPERATORS or s in "()":
            yield s
        elif s in ' ':  # garbage
            if number:
                yield float(number)
                number = ''
        else:
            param += s


        # elif number:  # если символ не цифра, то выдаём собранное число и начинаем собирать заново
        #     yield float(number)
        #     number = ''
        # if s in OPERATORS or s in "()":  # если символ - оператор или скобка, то выдаём как есть
        #     yield s
    if number:  # если в конце строки есть число, выдаём его
        yield float(number)