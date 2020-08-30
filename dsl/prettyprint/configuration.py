from .printer import Printer
from .processors import *
from .rules import Rules

PRIMITIVE_TYPES = ['bool', 'int', 'long', 'float', 'str']

DEFAULT_RULES = {
    Rules.STATEMENT_END: '',
    Rules.BLOCK_START: '{',
    Rules.BLOCK_END: '}',
    Rules.USE_SPACES: True,
    Rules.TAB_WIDTH: 4,
    Rules.STRUCTURES: {},
    Rules.NO_SPACING_OPERATORS: ['++', '--'],
}


class Configuration:
    def __init__(self, rules=None):
        self.rules = DEFAULT_RULES
        if rules:
            self.rules.update(rules)
        self.printer = Printer(self)
        self.class_processor_mapping = {}
        self._map_processors_to_classes()

    def get_structure_rules(self, structure_name):
        return self.rules[Rules.STRUCTURES][structure_name]

    def _map_processors_to_classes(self):
        self.class_processor_mapping.update(dict.fromkeys(self._get_list_of_structures(), structure))
        self.class_processor_mapping.update(dict.fromkeys(PRIMITIVE_TYPES, value))
        self.class_processor_mapping.update({
            'ComplexExp': expression,
            'AssignmentExp': expression,
            'UnaryExp': expression,
            'Statement': statement,
            'Op': operator,
            'UnaryOp': nospacing_operator,
            'AssignmentOp': operator,
            'Block': block,
            'Structure': structure,
        })

    def _get_list_of_structures(self):
        return self.rules[Rules.STRUCTURES].keys()