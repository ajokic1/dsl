from textx import metamodel_from_file
from textx.export import model_export


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

            process_format_rules(r.formats)
        elif r.__class__.__name__ == "OperatorRuleFormat":
            print("Operators :")
            for o in r.operators:
                print(o)
            print("Operator spacing: " + str(r.spacing))


def process_format_rules(formats):
    structure_rules = 'Structure\n\t:'
    helper_rules = []
    for f in formats:
        structure_rules += f.main_structure[len(f.main_structure.split(':')[0]) + 1:len(
        f.main_structure) - 1] + '\n\t|'
        helper_rules.append(f.helper_structures)
    structure_rules = structure_rules[0:len(structure_rules)-1] + ';'
    save_rules_in_file(structure_rules, helper_rules)


def save_rules_in_file(structure_rules, helper_rules):
    with open('user_grammar.tx', 'w') as user_grammar_file:
        basic_grammar_rules = get_predefined_rules()
        user_grammar_file.write(basic_grammar_rules + '\n\n' + structure_rules)
        for r in helper_rules:
            user_grammar_file.write('\n\n' + r)


def get_predefined_rules():
    with open('basic_grammar.tx', 'r') as f:
        return f.read()


if __name__ == '__main__':
    path = 'example.txt'
    model = create_model(path)
    showDataFromModel(model)

    format_metamodel = metamodel_from_file('user_grammar.tx')
    format_model = format_metamodel.model_from_file('file.txt')
    model_export(format_model, 'model.dot')
