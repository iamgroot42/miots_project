"""
    Source: https://rahul.gopinath.org/post/2020/08/20/control-flow-bytecode/
"""
from bytecode import Bytecode, ControlFlowGraph, dump_bytecode
import dis
from bytecode import ControlFlowGraph, dump_bytecode


if __name__ == "__main__":
    source_py = "augment.py"

    with open(source_py) as f_source:
        source_code = f_source.read()

    byte_code = compile(source_code, source_py, "exec")
    generator = dis.get_instructions(byte_code)

    bc = Bytecode.from_code(byte_code)

    blocks = ControlFlowGraph.from_bytecode(bc)
    dump_bytecode(bc)
    
    # TODO : Represent CFG as meaningful graph structure
