from textx import metamodel_from_file, metamodel_for_language, get_children_of_type, get_children
from textx import metamodel_from_str
from dsl.prettyprint import get_rules_from_model, pprint_to_string
import re
from textx.export import model_export


def create_model(path):
    metamodel = metamodel_from_file('grammar.tx')
    model = metamodel.model_from_file(path)
    return model


def showDataFromModel(model):
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


def selector(obj):
    return True


def prettyprint(rules_model, code_model):
    rules = get_rules_from_model(rules_model)
    result = pprint_to_string(code_model, rules)
    print(result)
    # structure = code_model.statements[3].statement
    # print(vars(structure))


if __name__ == '__main__':
    path = 'example.txt'
    model = create_model(path)
    showDataFromModel(model)

    format_metamodel = metamodel_from_file('user_grammar.tx')
    format_model = format_metamodel.model_from_file('file.txt')
    model_export(format_model, 'model.dot')

    prettyprint(model, format_model)
