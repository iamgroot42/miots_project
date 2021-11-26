import numpy as np
import re


def swap_setop_arguments(line, until_word):
    """
        Count number of open brackets until specified word inside a line
    """
    # Pick random position for a match for until_word
    positions = [m.start() for m in re.finditer(until_word, line)]
    # Pick random position
    if len(positions) > 0:
        position = positions[np.random.randint(len(positions))]
    else:
        raise AssertionError("%s not found in %s" % (until_word, line))
    
    # Start going back from position to find what variable the function is called on

    position_clone = position - 1
    pasta_copy = ""
    count = 0
    while position_clone >= 0:
        if line[position_clone] == '(':
            count += 1
        elif line[position_clone] == ')':
            count -= 1

        pasta_copy += line[position_clone]

        if count == 0 and (line[position_clone] in [' ', '.', ',', '(', '[', '{']):
            break
        position_clone -= 1
    
    position_clone = max(position_clone, 0)
    pasta_copy = pasta_copy[::-1]

    count_match = 0
    for i in line[:position]:
        if i == '(':
            count_match += 1
        elif i == ')':
            count_match -= 1
    position_start = position + len(until_word)
    copy_pasta = ""
    
    # Find all characters until this level of bracket ends
    count = count_match
    while position_start < len(line):
        if count == count_match and (line[position_start] in [' ', '.', ',', ')', ']', '}']):
            break

        if line[position_start] == ')':
            count -= 1
        elif line[position_start] == '(':
            count += 1
        
        copy_pasta += line[position_start]
            
        position_start += 1
    
    # For a (a).until_word(b) call, replace it with
    # a (b).until_word(a) call. Take special care to match
    # brackets properly

    print(line[:position_clone], "|", copy_pasta, "|", until_word, "|", pasta_copy, "|", line[position_start:])

    new_line = line[:position_clone] + copy_pasta.rstrip(
        ' ') + until_word + "(" + pasta_copy.lstrip(' ') + ")" + line[position_start:]
    new_line += "  # Changed via automated augmentation"

    return new_line


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
