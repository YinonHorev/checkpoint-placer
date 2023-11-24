import pytest

from src.parser import parse_dot_to_digraph


def test_dot_parser():
    dot_str = "digraph graphname{\n1->2\n2->3\n2->5\n5->2\n3->5}}"
    G = parse_dot_to_digraph(dot_str)
    assert G.number_of_nodes() == 4
