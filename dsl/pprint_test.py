import os
from os.path import dirname, join
from dsl.prettyprint import pprint_to_string
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export

THIS_FOLDER = dirname(__file__)
PRETTYPRINT_FOLDER = join(THIS_FOLDER, 'prettyprint')
PRETTYPRINT_TEST_FOLDER = join(PRETTYPRINT_FOLDER, 'test')

def main(debug=False):
    mm = metamodel_from_file(join(PRETTYPRINT_TEST_FOLDER, 'gramatika.tx'), debug=debug)
    proba_model = mm.model_from_file(join(PRETTYPRINT_TEST_FOLDER, 'proba.java'))
    export_dot(mm, proba_model)
    result = pprint_to_string(proba_model, {})
    print(result)


def export_dot(mm, model):
    dot_folder = PRETTYPRINT_TEST_FOLDER
    if not os.path.exists(dot_folder):
        os.mkdir(dot_folder)
    metamodel_export(mm, join(dot_folder, 'metamodel.dot'))
    model_export(model, join(dot_folder, 'model.dot'))


if __name__ == "__main__":
    main()