from .printer import Printer
from .processors import *

PRIMITIVE_TYPES = ['bool', 'int', 'long', 'float', 'str']

DEFAULT_RULES = {
    'statement_end': '',
    'block_start': '{',
    'block_end': '}',
    'use_spaces': True,
    'tab_width': 4,
    'structures': {},
    'no_spacing_operators': ['++', '--'],
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
        return self.rules['structures'][structure_name]


    def _map_processors_to_classes(self):
        self.class_processor_mapping.update(dict.fromkeys(self._get_list_of_structures(), structure))
        self.class_processor_mapping.update(dict.fromkeys(PRIMITIVE_TYPES, value))
        self.class_processor_mapping.update({
            'Program': program,
            'Expression': expression,
            'Statement': statement,
            'Operator': operator,
            'Block': block,
        })


    def _get_list_of_structures(self):
        return self.rules['structures'].keys()