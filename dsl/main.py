from textx import metamodel_from_file

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
                print("Boundaries: " + r.block_elem.boundaries.bound)
                print("Begin mark: " + r.block_elem.begin.begin)
                print("End mark: " + r.block_elem.end.end)
                print("Indent: " + str(r.block_elem.indent.indent_num))

            for f in r.formats:
                print("Structure format is: " + f.structure_format)
        elif r.__class__.__name__ == "OperatorRuleFormat":
            print("Operators :")
            for o in r.operators:
                print(o)
            print("Operator spacing: " + str(r.spacing))


if __name__ == '__main__':
    path = 'example.txt'
    model = create_model(path)
    showDataFromModel(model)
