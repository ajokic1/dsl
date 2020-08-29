from .processors import process_node
from .configuration import Configuration

def pprint_to_string(root_node, rules):
    return _pprint(root_node, rules).printer.result

def pprint_to_file(filename, root_node, rules):
    _pprint(root_node, rules).printer.write_to_file(filename)

def _pprint(root_node, rules):
    configuration = Configuration(rules)
    process_node(configuration, root_node)
    return configuration