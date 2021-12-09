import  tokenize
from io import StringIO
import networkx as nx
import numpy as np
import re
import dis


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


def remove_comments_and_docstrings(source):
    """
        Returns 'source' minus comments and docstrings.
    """
    io_obj = StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        ltext = tok[4]
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
        # Remove comments:
        if token_type == tokenize.COMMENT:
            pass
        # This series of conditionals removes docstrings:
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
                # This is likely a docstring; double-check we're not inside an operator:
                if prev_toktype != tokenize.NEWLINE:
                    if start_col > 0:
                        out += token_string
        else:
            out += token_string
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
    temp = []
    for x in out.split('\n'):
        if x.strip() != "":
            temp.append(x)
    return '\n'.join(temp)


# For CFG-related code (two classes below)
# Source: https://rahul.gopinath.org/post/2020/08/20/control-flow-bytecode/
class CFGNode:
    def __init__(self, i, bid):
        self.i = i
        self.bid = bid
        self.children = []
        self.props = {}

    def add_child(self, n):
        self.children.append(n)


class CFG:
    def __init__(self, byte_code):
        def lstadd(hmap, key, val):
            if key not in hmap:
                hmap[key] = [val]
            else:
                hmap[key].append(val)
        enter = CFGNode(dis.Instruction(
            'NOP', opcode=dis.opmap['NOP'], arg=0, argval=0, argrepr=0, offset=0, starts_line=0, is_jump_target=False), 0)
        last = enter
        self.jump_to = {}
        self.opcodes = {}
        for i, ins in enumerate(dis.get_instructions(byte_code)):
            byte = i * 2
            node = CFGNode(ins, byte)
            self.opcodes[byte] = node
            if ins.opname in ['LOAD_CONST', 'LOAD_FAST', 'STORE_FAST', 'COMPARE_OP', 'INPLACE_ADD', 'INPLACE_SUBTRACT', 'RETURN_VALUE', 'BINARY_MODULO', 'POP_BLOCK']:
                last.add_child(node)
                last = node
            elif ins.opname == 'POP_JUMP_IF_FALSE':
                lstadd(self.jump_to, ins.arg, node)
                node.props['jmp'] = True
                last.add_child(node)
                last = node
            elif ins.opname == 'JUMP_FORWARD':
                node.props['jmp'] = True
                lstadd(self.jump_to, (i+1)*2 + ins.arg, node)
                last.add_child(node)
                last = node
            elif ins.opname == 'SETUP_LOOP':
                last.add_child(node)
                last = node
            elif ins.opname == 'JUMP_ABSOLUTE':
                lstadd(self.jump_to, ins.arg, node)
                node.props['jmp'] = True
                last.add_child(node)
                last = node
            # Else, not a jump (not relevant)
        for byte in self.opcodes:
            if byte in self.jump_to:
                node = self.opcodes[byte]
                assert node.i.is_jump_target
                for b in self.jump_to[byte]:
                    b.add_child(node)

    def to_graph(self):
        G = nx.DiGraph()
        for nid, cnode in self.opcodes.items():
            G.add_node(str(cnode.bid), label="%d: %s" % (nid, cnode.i.opname))
            for cn in cnode.children:
                G.add_edge(str(cnode.bid), str(cn.bid))
        # Remove all isolated nodes
        G.remove_nodes_from(list(nx.isolates(G)))
        return G
