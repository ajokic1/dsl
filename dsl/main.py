from textx import *
from textx.export import model_export
from prettyprint import *
import re


def main():
    rules_model = handle_file_oserror(load_rules_file)
    format_model = handle_file_oserror(load_input_file)
    handle_file_oserror(create_output_file, rules_model, format_model)
    

def handle_file_oserror(callback, *args):
    result = None
    while True:
        try:
            result = callback(*args)
            break
        except OSError:
            print ("Could not open/read file")
            continue
    return result


def load_rules_file(*args):
    rules_path = input("Rules file path: ")
    rules_model = create_rules_model(rules_path)
    analyze_rules_model(rules_model)
    return rules_model


def load_input_file(*args):
    input_path = input("Input file path: ")
    format_metamodel = metamodel_from_file('user_grammar.tx')
    format_model = format_metamodel.model_from_file(input_path)
    model_export(format_model, 'model.dot')
    return format_model


def create_output_file(*args):
    output_path = input("Output file path: ")
    prettyprint(*args, output_path)


def create_rules_model(path):
    metamodel = metamodel_from_file('grammar.tx')
    model = metamodel.model_from_file(path)
    return model


def analyze_rules_model(model):
    rules = model.rules
    formats = []
    operators = {'spacing': [], 'no_spacing': []}
    for r in rules:
        if r.__class__.__name__ == "StructureFormatRule":
            print("Rule caption: " + r.caption)
            if r.block_elem != None:
                if r.block_elem.boundaries != None:
                    print("Boundaries: " + r.block_elem.boundaries.bound)
                if r.block_elem.begin != None:
                    print("Begin mark: " + r.block_elem.begin.begin)
                if r.block_elem.end != None:
                    print("End mark: " + r.block_elem.end.end)
                if r.block_elem.indent != None:
                    print("Indent: " + str(r.block_elem.indent.indent_num))

            formats += r.formats
        elif r.__class__.__name__ == "OperatorRuleFormat":
            if r.spacing:
                operators['spacing'] += r.operators
            else:
                operators['no_spacing'] += r.operators
            print("Operators :")
            for o in r.operators:
                print(o)
            print("Operator spacing: " + str(r.spacing))
    process_rules(formats, operators)


def process_rules(formats, operators):
    structure_rules = 'Structure\n\t:'
    helper_rules = []
    for f in formats:
        structure_rules += f.main_structure[len(f.main_structure.split(':')[0]) + 1:len(
            f.main_structure) - 1] + '\n\t|'
        helper_rules.append(f.helper_structures)
    structure_rules = structure_rules[0:len(structure_rules) - 1] + ';'
    operator_rules = process_operator_rules(operators)
    helper_rules += operator_rules
    save_rules_in_file(structure_rules, helper_rules)


def process_operator_rules(operators):
    operator_rules = [generate_operator_rule('Op', operators['spacing']),
                      generate_operator_rule('UnaryOp', operators['no_spacing'])]
    return operator_rules


def generate_operator_rule(classname, operators):
    rule = classname + ': '
    for op in operators:
        rule += 'op=\'' + op + '\'' + '|'
    rule = rule.rstrip('|')
    rule += ';'
    return rule


def save_rules_in_file(structure_rules, helper_rules):
    with open('user_grammar.tx', 'w') as user_grammar_file:
        basic_grammar_rules = get_predefined_rules()
        user_grammar_file.write(basic_grammar_rules + '\n\n' + structure_rules)
        for r in helper_rules:
            user_grammar_file.write('\n\n' + r)


def get_predefined_rules():
    with open('basic_grammar.tx', 'r') as f:
        return f.read()


def prettyprint(rules_model, code_model, output):
    rules = get_rules_from_model(rules_model)
    result = pprint_to_file(output, code_model, rules)
    print(result)


if __name__ == '__main__':
    main()