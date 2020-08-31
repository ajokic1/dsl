from enum import Enum


class Rules(Enum):
    STATEMENT_END = 'statement_end'
    BLOCK_START = 'block_start'
    BLOCK_END = 'block_end'
    USE_SPACES = 'use_spaces'
    TAB_WIDTH = 'tab_width'
    STRUCTURES = 'structures'
    NO_SPACING_OPERATORS = 'no_spacing_operators'


def get_rules_from_model(model):
    rules = {}
    structures = {}
    for rule in model.rules:
        process_rule(rule, rules, structures)

    rules[Rules.STRUCTURES] = structures
    return rules


def process_rule(rule, rules, structures):
    if rule.__class__.__name__ == "StructureFormatRule":
        if rule.caption == "global":
            process_global_rule(rule, rules)
        else:
            process_structure_rule(rule, structures)


def process_structure_rule(rule, rules_dict):
    structure = {}
    # TODO: process structure-specific rules
    rules_dict[rule.caption] = structure


def process_global_rule(rule, rules_dict):
    if rule.block_elem is not None:
        process_block_rule(rule, rules_dict)


def process_block_rule(rule, rules_dict):
    if rule.block_elem.begin is not None:
        rules_dict[Rules.BLOCK_START] = rule.block_elem.begin.begin
    if rule.block_elem.end is not None:
        rules_dict[Rules.BLOCK_END] = rule.block_elem.end.end
    if rule.block_elem.indent is not None:
        rules_dict[Rules.TAB_WIDTH] = rule.block_elem.indent.indent_num