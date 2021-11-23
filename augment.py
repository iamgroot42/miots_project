"""
    Take a codefile and augment it with changes that preserve functionality.
    Used for data-augmentation to improve model generalization.
"""
import random
from utils import figure_out_intend_size, wanted_condition


JUNK_TO_ADD = [
    [("if (4 == 1):", 0), ("hoolahoop = 7", 1)],
    [("if (3 == 3):", 0), ("boolaboop = 9", 1)]
]

RANDOM_FUNCTIONS = [

]

def add_random_line(lines):
    """
        Find a line that doesn't have unclosed brackets or a colon at the end
        Or an unclosed if/else series of statements.
        Add a new junk line with a semicolon.
        Ignore comments.
    """

    # Find eligible lines
    eligible_lines = [i for i, line in enumerate(lines) if wanted_condition(line)]
    # Pick a line at random
    line_index = eligible_lines[random.randint(0, len(eligible_lines) - 1)]
    # Figure out if indentation has spaces or tabs
    if lines[line_index].startswith('\t'):
        indent_char = '\t'
        indent_size = 1
    else:
        indent_size = figure_out_intend_size(lines)
        indent_char = ' '
    # Copy level of indentation
    indent_level = (len(lines[line_index]) - len(lines[line_index].lstrip(indent_char))) // indent_size
    junk_to_add = JUNK_TO_ADD[random.randint(0, len(JUNK_TO_ADD) - 1)]
    # If 3 lines, add first, indented second, third
    # Else, simple add line
    for i, (jta, il) in enumerate(junk_to_add):
        lines.insert(line_index + i + 1, indent_char * indent_size * (indent_level + il) + jta)
    # if len(junk_to_add) == 2:
    #     lines.insert(line_index + 1, indent_char * indent_size * indent_level + junk_to_add[0])
    #     lines.insert(line_index + 2, indent_char * indent_size * (indent_level + 1) + junk_to_add[1])
    # else:
    #     lines.insert(line_index + 1, indent_char * indent_size * indent_level + junk_to_add[0])
    # Return augmented line
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


if __name__ == "__main__":
    with open("utils.py") as f:
        lines = f.read().splitlines()
    lines_to_write = junk_line_addition(lines)
    with open("utils_edited.py", "w") as f:
        for line in lines_to_write:
            f.write(line + "\n")
