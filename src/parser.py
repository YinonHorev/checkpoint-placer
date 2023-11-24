import networkx as nx
import pydot


def parse_dot_to_digraph(dot_string):
    graphs = pydot.graph_from_dot_data(dot_string)
    dot_graph = graphs[0]
    G = nx.nx_pydot.from_pydot(dot_graph)
    return G
