"""
    Source: https://rahul.gopinath.org/post/2020/08/20/control-flow-bytecode/
"""
import utils
import networkx as nx
import matplotlib.pyplot as plt


if __name__ == "__main__":
    source_py = "augment.py"

    with open(source_py) as f_source:
        source_code = f_source.read()
    
    # Remove comments and docstrings
    source_code = utils.remove_comments_and_docstrings(source_code)
    byte_code = compile(source_code, source_py, "exec")

    # Extracf CFG in networkx format
    v = utils.CFG(byte_code)
    g = v.to_graph()

    # Visualize CFG
    nx.draw(g, with_labels=True)
    plt.axis('off')
    plt.show()
    plt.savefig("./augment_cfg.png")
