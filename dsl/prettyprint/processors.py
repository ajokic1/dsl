def process_node(config, node):
    processor_function = config.class_processor_mapping[node.__class__.__name__]
    processor_function(config, node)


def process_children(config, children):
    for child in children:
        process_node(config, child)


def program(config, node):
    process_children(config, node.children)


def structure(config, node):
    structure_header(config, node)
    block(config, node)


def structure_header(config, node):
    if config.get_structure_rules(node.__class__.__name__).get('no_newline'):
        config.printer.append(' ')
    else:
        config.printer.new_line_indent()
    process_children(config, node.children)


def block(config, node):
    config.printer.new_line_indent() #remove
    value(config, node.block_header) #remove
    config.printer.append(config.rules['block_start'])
    config.printer.increase_indent()
    process_children(config, node.children)
    config.printer.decrease_indent()
    if config.rules['block_end']:
        config.printer.new_line_indent()
        config.printer.append(config.rules['block_end'])


def statement(config, node):
    config.printer.new_line_indent()
    #process_children(config, node.children)
    value(config, node.text) #remove
    if config.rules['statement_end']:
        config.printer.append(config.rules['statement_end'])


def function(config, node):
    value(node.name)
    config.printer.append('(')
    for i, parameter in node.parameters:
        process_node(parameter)
        if i != len(node.parameters) - 1:
            config.printer.append(', ')
    config.printer.append(')')


def expression(config, node):
    process_children(config, node.children)


def value(config, node_value):
    config.printer.append(node_value)


def operator(config, node):
    if node.value in config.rules['no_spacing_operators']:
        value(config, node.value)
    else:
        config.printer.append(' ')
        value(config, node.value)
        config.printer.append(' ')