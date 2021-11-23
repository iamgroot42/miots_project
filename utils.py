import numpy as np


def matched(str, brackets=('(', ')')):
    count = 0
    for i in str:
        if i == brackets[0]:
            count += 1
        elif i == brackets[1]:
            count -= 1
        if count < 0:
            return False
    return count == 0

def ongoing_if_else(lines):
    # Look at lines in reverse, identify post 'else' and pre 'if' areas
    # Mark them as safe to add junk
    counts = []
    for line in lines:
        if line.startswith('if'):
            counts.append(1)
        elif line.startswith('else'):
            counts.append(-1)
        else:
            counts.append(0)

    counts.reverse()
    for i in range(1, len(counts)):
        counts[i] += counts[i - 1]
    counts.reverse()


def figure_out_intend_size(lines):
    # Find a line that ends with colon
    # Figure difference in indentation between that line and the next line
    # Return that difference
    for i, line in enumerate(lines):
        if line.endswith(":"):
            if i + 1 < len(lines):
                first_indent_level = len(line) - len(line.lstrip(' '))
                second_indent_level = len(lines[i + 1]) - len(lines[i + 1].lstrip(' '))
                return second_indent_level - first_indent_level


def wanted_condition(l):
    conditions = []
    conditions.append(matched(l))
    conditions.append(not l.startswith('#'))
    conditions.append(matched(l, ('{', '}')))
    conditions.append(matched(l, ('[', ']')))
    conditions.append(not l.lstrip(' ').lstrip('\t').startswith("#"))
    conditions.append(not l.lstrip(' ').lstrip('\t').startswith("return "))
    return np.logical_and.reduce(conditions)
