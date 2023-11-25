from src.algo import PathAnalyser
from src.api import PathAnalysisRequest
from src.parser import parse_dot_to_digraph

def test_simple_path_analyser():
    G = parse_dot_to_digraph("digraph graphname{\n1->2\n2->3\n2->5\n5->2\n3->5}")
    e1 = "1"
    h = "5"
    analyser = PathAnalyser()
    analyser(G, e1, h)
    assert analyser.result == {"1", "2"}

def test_h_is_not_last_in_dfs():
    G = parse_dot_to_digraph("digraph graphname{\n1->2\n2->3\n2->5\n5->2\n3->5\n5->6}")
    e1 = "1"
    h = "5"
    analyser = PathAnalyser()
    analyser(G, e1, h)
    assert analyser.result == {"1", "2"}


def test_alog_1():
    G = parse_dot_to_digraph("digraph graphname{\n1->2\n1->3\n3->4\n2->4\n4->9\n4->5\n4->7\n5->6\n6->7\n7->8}")
    e1 = "1"
    h = "8"
    analyser = PathAnalyser()
    analyser(G, e1, h)
    assert analyser.result == {"1", "4", "7"}
