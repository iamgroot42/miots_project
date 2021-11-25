"""
    Take a codefile and augment it with changes that preserve functionality.
    Used for data-augmentation to improve model generalization.
"""
import random
import utils


JUNK_TO_ADD = [
    [("if (4 == 1):", 0), ("hoolahoop = 7", 1)],
    [("if (3 == 3):", 0), ("boolaboop = 9", 1)],
    [("print(42)", 0)],
    [("boolaboop = 10", 0), ("while boolaboop > 0:", 0), ("boolaboop -= 1", 1)],
]

def add_random_line(lines):
    """
        Find a line that doesn't have unclosed brackets or a colon at the end
        Or an unclosed if/else series of statements.
        Add a new junk line with a semicolon.
        Ignore comments.
    """

    # Find eligible lines
    eligible_lines = [i for i, line in enumerate(lines) if utils.wanted_condition(line)]

    if len(eligible_lines) == 0:
        return lines

    # Pick a line at random
    line_index = eligible_lines[random.randint(0, len(eligible_lines) - 1)]
    # Figure out if indentation has spaces or tabs
    if lines[line_index].startswith('\t'):
        indent_char = '\t'
        indent_size = 1
    else:
        indent_size = utils.figure_out_intend_size(lines)
        indent_char = ' '
    # Copy level of indentation
    indent_level = (len(lines[line_index]) - len(lines[line_index].lstrip(indent_char))) // indent_size
    junk_to_add = JUNK_TO_ADD[random.randint(0, len(JUNK_TO_ADD) - 1)]
    # If 3 lines, add first, indented second, third
    # Else, simple add line
    comment_added = "  # Changed via automated augmentation"
    for i, (jta, il) in enumerate(junk_to_add):
        lines.insert(line_index + i + 1, indent_char *
                     indent_size * (indent_level + il) + jta + comment_added)
    return lines


def add_random_function(lines, n_times):
    """
        Define random function that does not do any useful compute,
        and then call it randomly from within the file
    """


def add_random_function_call(lines):
    """
        Add library (may or may not be usedf) and make a function call to it
    """


def _interchange_set_fn(lines, op_type=".union"):
    """
        Interchange caller and argument for set function,
        Since a U b etc is same as b U a
    """

    # Find eligible lines
    eligible_lines = [i for i, line in enumerate(lines) if utils.wanted_condition(line)]
    eligible_lines = [i for i in eligible_lines if op_type in lines[i]]

    if len(eligible_lines) == 0:
        return lines

    # Pick a line at random
    line_index = eligible_lines[random.randint(0, len(eligible_lines) - 1)]

    # Edit line to swap out argument and caller
    lines[line_index] = utils.swap_setop_arguments(lines[line_index], op_type)

    return lines


def interchange_union_fn(lines):
    return _interchange_set_fn(lines, ".union")


def interchange_intersection_fn(lines):
    return _interchange_set_fn(lines, ".intersection")


RANDOM_FUNCTIONS = [
    interchange_union_fn,
    interchange_intersection_fn
]

if __name__ == "__main__":
    with open("dummy.py") as f:
        lines = f.read().splitlines()
    # lines_to_write = interchange_intersection_fn(lines)
    lines_to_write = add_random_line(lines)
    with open("dummy_out.py", "w") as f:
        for line in lines_to_write:
            f.write(line + "\n")
