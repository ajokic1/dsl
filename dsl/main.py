from textx import metamodel_from_file, metamodel_for_language
from textx import metamodel_from_str
from dsl.prettyprint import get_rules_from_model
import re


def create_model(path):
    metamodel = metamodel_from_file('grammar.tx')
    model = metamodel.model_from_file(path)
    return model

def showDataFromModel(model):
    rules = model.rules
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

            for f in r.formats:
                process_format_rule(f)

        elif r.__class__.__name__ == "OperatorRuleFormat":
            print("Operators :")
            for o in r.operators:
                print(o)
            print("Operator spacing: " + str(r.spacing))


def process_format_rule(f):
    before_rule = 'Before: /(?ms).*?(?=if)/ ;'
    after_rule = 'After: /(?ms)(?!if).*?(?=if)/| /(?ms)(?!if).*(?=if)?/| \'\' ;'

    main_struct_name = f.main_structure.split(':')[0]
    main_struct = main_struct_name + ':Before?-' + f.main_structure[len(main_struct_name) + 1:len(
        f.main_structure) - 1] + 'After?-;'
    match_rule = 'Match: matches*=' + main_struct_name + '[\'\'];'
    helper_rules = re.sub(r"[\t\n]*", "", f.helper_structures)

    with open(main_struct_name + 'Format.tx', 'w') as f:
        f.write(match_rule + '\n' + main_struct + '\n' + before_rule + '\n' + after_rule + '\n' + helper_rules.strip())

    # extract structures to be formatted (format_model.matches)
    format_metamodel = metamodel_from_file(main_struct_name + 'Format.tx')
    format_model = format_metamodel.model_from_file('file.txt')
    print('------------------')
    print(format_model.matches)
    print('------------------')


def prettyprint(rules_model):
    rules = get_rules_from_model(rules_model)
    # TODO: pprint model of code


if __name__ == '__main__':
    path = 'example.txt'
    model = create_model(path)
    prettyprint(model)
    showDataFromModel(model)

