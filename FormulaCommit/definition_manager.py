from FormulaCommit.parse_sql import ParseSqlManager


class DefinitionManager:

    def __init__(self):
        self.__parser_manager = ParseSqlManager()
        self.__definition_and_field = {}  # словарь определений и полей
        self.__symbols_and_definition_numbers_by_lazy = None
        self.__symbols_and_field = {}  # todo переделать в dataclass

    @property
    def symbols_and_definition_numbers(self):
        if self.__symbols_and_definition_numbers_by_lazy is None:
            self.__symbols_and_definition_numbers_by_lazy = {}
            for number_definition, definition in self.__definition_and_field.items():
                for symbol in definition.all_definitions_symbols:
                    if symbol in self.__symbols_and_definition_numbers_by_lazy:
                        self.__symbols_and_definition_numbers_by_lazy.get(symbol).append(number_definition)
                    else:
                        self.__symbols_and_definition_numbers_by_lazy.update({symbol: [number_definition]})
            return self.__symbols_and_definition_numbers_by_lazy
        else:
            return self.__symbols_and_definition_numbers_by_lazy

    @property
    def all_field_dependencies_from_formula_symbol(self):
        return dict(map(lambda x: (x[0], x[1].dependence), self.__symbols_and_field.items()))

    def get_formula_by_symbol(self, symbol):
        return self.__parser_manager.parameter_for_calculating_the_result(current_field=
                                                                          self.__symbols_and_field[symbol])

    def get_field_by_symbol(self, symbol):
        return self.__symbols_and_field.get(symbol)

    def add(self, current_field):
        if self.__definition_and_field.get(current_field.definition_number):
            definition = self.__definition_and_field[current_field.definition_number]
            definition.add_field(current_field)
        else:
            definition = Definition()
            definition.add_field(current_field)
            self.__definition_and_field.update({current_field.definition_number: definition})

    def update_data_for_calculating(self):
        for definition_number, definition in self.__definition_and_field.items():
            for symbol, current_field in definition.field.items():
                if current_field.formula:
                    current_field.formula = self.__parser_manager.update_formula(
                        current_field,
                        self.symbols_and_definition_numbers)
                    current_field.dependence = self.__parser_manager.update_dependence(current_field.formula)
            self.__symbols_and_field.update(dict(map(lambda items: (items[1].symbol_item.symbol_and_definition,
                                                                    items[1]),
                                                     definition.field.items())))


class Definition:
    def __init__(self):
        self.__check_ignore = False
        self.__input_manual = False
        self.__field = {}
        self.__all_definitions_symbols = set()

    @property
    def check_ignore(self):
        return self.__check_ignore

    @property
    def input_manual(self):
        return self.__input_manual

    @property
    def field(self):
        return self.__field

    @property
    def all_definitions_symbols(self):
        return self.__all_definitions_symbols

    def add_field(self, current_field):
        if self.__input_manual:
            current_field._value_only = True
        if not current_field.symbol_item.symbol:  # Если нет symbol создаем symbol_and_definition чтобы расчитать value
            self.create_field_symbol(current_field)
        if not self.__check_ignore:
            self.__all_definitions_symbols.add(current_field.symbol_item.symbol)

        if 'check_ignore' in current_field.symbol_item.symbol and current_field.value:
            self.__check_ignore = True
            self.__all_definitions_symbols.clear()
        elif 'input_manual' in current_field.symbol_item.symbol and current_field.value:
            self.__input_manual = True
            self.__all_definitions_symbols.clear()

        self.__field.update({current_field.symbol_item.symbol: current_field})

    def create_field_symbol(self, current_field):
        current_field.symbol_item.symbol = f'@{len(self.__field)}'
        current_field.symbol_item.symbol_and_definition = f'@{len(self.__field)}_{current_field.definition_number}'
        current_field.symbol_item.overridden = True
