class AbstractField:
    def __init__(self):
        self._symbol = None
        self._formula = None
        self._value = None
        self._dependence = set()

    @property
    def dependence(self):
        """
        Getter _dependence, обращаться как к атрибуту
        :return: Множество всех существующих символьных обозначений в формуле
        """
        return self._dependence

    @dependence.setter
    def dependence(self, value):
        """
        Setter _dependence, обращаться как к переменной
        :param value: Множество элементов
        """
        self._dependence = value

    @property
    def formula(self):
        """
        Getter _formula, обращаться как к атрибуту
        :return: Строка с формулой
        """
        return self._formula

    @formula.setter
    def formula(self, value):
        """
        Setter _formula, обращаться как к переменной
        :param value: Строка с формулой
        """
        self._formula = value


class IntegerField(AbstractField):

    def __init__(self, *, symbol, formula, value=None, opred_number=1, value_only=False):
        super().__init__()
        self._symbol = symbol
        self._formula = formula
        self._value = value
        self._opred_number = opred_number
        self._value_only = value_only

    def calc(self):
        self._value = float(eval(str(self._value)))  # Расчет, округление
        return self._value


class StringField(AbstractField):

    def __init__(self, *, symbol, formula, value=None, opred_number=1):
        super().__init__()
        self._symbol = symbol
        self._formula = formula
        self._value = value
        self._opred_number = opred_number

    def calc(self):
        return self._value


class FloatField(AbstractField):

    def __init__(self, *, symbol, formula):
        super().__init__()
        self._symbol = symbol
        self._type = float
        self._formula = formula
