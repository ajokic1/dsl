from textx import get_children, get_parent_of_type, get_children_of_type

from .rules import Rules

def process_node(config, node):
    processor_function = config.class_processor_mapping[node.__class__.__name__]
    processor_function(config, node)


def process_children(config, children):
    for child in children:
        process_node(config, child)


def process_all_children(config, node):
    process_children(config, get_children_of_type('str', node))


def block(config, node):
    if not get_parent_of_type('Structure', node):
        process_children(config, node.statements)
    else:
        config.printer.append(' ')
        config.printer.append(config.rules[Rules.BLOCK_START])
        config.printer.increase_indent()
        process_children(config, node.statements)
        config.printer.decrease_indent()
        if config.rules[Rules.BLOCK_END]:
            config.printer.new_line_indent()
            config.printer.append(config.rules[Rules.BLOCK_END])


def statement(config, node):
    config.printer.new_line_indent()
    process_node(config, node.statement)


def structure(config, node):
    for key, value in vars(node).items():
        if key not in ['_tx_position', '_tx_position_end', 'parent']:
            process_node(config, value)


def expression(config, node):
    for part in node.part:
        process_node(config, part)

# def function(config, node):
#     value(node.name)
#     config.printer.append('(')
#     for i, parameter in node.parameters:
#         process_node(parameter)
#         if i != len(node.parameters) - 1:
#             config.printer.append(', ')
#     config.printer.append(')')


def value(config, node_value):
    config.printer.append(node_value)

def nospacing_operator(config, node):
    value(config, node.op)

def operator(config, node):
        config.printer.append(' ')
        value(config, node.op)
        config.printer.append(' ')


# Uvijek vraca true - za textx get_children
def selector(obj):
    return True