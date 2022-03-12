from collections import defaultdict
from typing import Any

from FormulaCommit.parse_sql import ParseSqlManager


class DefinitionManager:

    def __init__(self):
        self.__parser_manager = ParseSqlManager()
        self.__definition_and_field: dict[int, Definition] = defaultdict(Definition)  # словарь определений и полей
        self.__symbols_and_definition_numbers_by_lazy: dict[int, list] = defaultdict(list)
        self.__symbols_and_field = {}

    @property
    def symbols_and_definition_numbers(self):
        if self.__symbols_and_definition_numbers_by_lazy:
            return self.__symbols_and_definition_numbers_by_lazy
        else:
            for number_definition, definition in self.__definition_and_field.items():
                for symbol in definition.all_definitions_symbols:
                    self.__symbols_and_definition_numbers_by_lazy[symbol].append(number_definition)
            return self.__symbols_and_definition_numbers_by_lazy

    @property
    def all_field_dependencies_from_formula_symbol(self):
        return dict(map(lambda field: (field[0], field[1].dependence), self.__symbols_and_field.items()))

    def get_formula_by_symbol(self, symbol):
        return self.__parser_manager.parameter_for_calculating_the_result(current_field=
                                                                          self.__symbols_and_field[symbol])

    def get_field_by_symbol(self, symbol):
        return self.__symbols_and_field.get(symbol)

    def add(self, current_field):
        definition = self.__definition_and_field[current_field.definition_number]
        definition.add_field(current_field)

    def update_data_for_calculating(self):
        for definition_number, definition in self.__definition_and_field.items():
            for symbol in definition.all_definitions_symbols:
                current_field = definition.field[symbol]
                if current_field.formula:
                    current_field.formula = self.__parser_manager.update_formula(
                        current_field,
                        self.symbols_and_definition_numbers)
                    current_field.dependence = set() if current_field._value_only else \
                        self.__parser_manager.update_dependence(current_field.formula)

                self.__symbols_and_field.update({current_field.symbol_item.symbol_and_definition: current_field})

    def update_value_for_data(self, data) -> dict:
        result = {}
        for definition_number, definition in self.__definition_and_field.items():
            for symbol in definition.all_definitions_symbols:
                current_field = definition.field[symbol]
                if current_field.symbol_item.symbol_and_definition in data:
                    current_field.value = data[current_field.symbol_item.symbol_and_definition]
                current_field.calc()
                result.update({current_field._primary_key: current_field.value})
        return result


class Definition:

    def __init__(self):
        self.__check_ignore = False
        self.__input_manual = False
        self.__field = {}
        self.__all_definitions_symbols = set()

    @property
    def field(self):
        return self.__field

    @property
    def all_definitions_symbols(self):
        return self.__all_definitions_symbols

    def add_field(self, current_field):
        if self.__input_manual:
            current_field._value_only = True
        if not current_field.symbol_item:  # Если у current_field не заполнен символ, создаем symbol_item
            self.create_field_symbol(current_field)
        if not self.__check_ignore:
            self.__all_definitions_symbols.add(current_field.symbol_item.symbol)
        if self.__check_ignore:
            current_field._value_only = True

        if 'check_ignore' in current_field.symbol_item.symbol and current_field.value:
            self.__check_ignore = True
            self.__all_definitions_symbols.clear()
        elif 'input_manual' in current_field.symbol_item.symbol and current_field.value:
            self.__input_manual = True
            self.__all_definitions_symbols.clear()

        self.__field.update({current_field.symbol_item.symbol: current_field})

    def create_field_symbol(self, current_field):
        current_field.create_symbol(f'@{len(self.__field)}')
