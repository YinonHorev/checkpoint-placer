import pytest
from networkx import DiGraph, path_graph

from src.algo import PathAnalyser
from src.parser import parse_dot_to_digraph
from src.strategy import (
    ArticulationSequenceComponentsStrategy,
    NaivePathAnalysisStrategy,
    PathAnalysisStrategy,
)


@pytest.mark.parametrize(
    "strategy", [NaivePathAnalysisStrategy, ArticulationSequenceComponentsStrategy]
)
def test_simple_path_analyser(strategy: PathAnalysisStrategy):
    G = parse_dot_to_digraph("digraph graphname{\n1->2\n2->3\n2->5\n5->2\n3->5}")
    e1 = "1"
    h = "5"
    analyser = PathAnalyser(strategy)
    assert analyser(G, e1, h) == {"1", "2"}


@pytest.mark.parametrize(
    "strategy", [NaivePathAnalysisStrategy, ArticulationSequenceComponentsStrategy]
)
def test_h_is_not_last_in_dfs(strategy: PathAnalysisStrategy):
    G = parse_dot_to_digraph("digraph graphname{\n1->2\n2->3\n2->5\n5->2\n3->5\n5->6}")
    e1 = "1"
    h = "5"
    analyser = PathAnalyser(strategy)
    assert analyser(G, e1, h) == {"1", "2"}


@pytest.mark.parametrize(
    "strategy", [NaivePathAnalysisStrategy, ArticulationSequenceComponentsStrategy]
)
def test_alog_1(strategy: PathAnalysisStrategy):
    G = parse_dot_to_digraph(
        "digraph graphname{\n1->2\n1->3\n3->4\n2->4\n4->9\n4->5\n4->7\n5->6\n6->7\n7->8}"
    )
    e1 = "1"
    h = "8"
    analyser = PathAnalyser(strategy)
    assert analyser(G, e1, h) == {"1", "4", "7"}


@pytest.mark.parametrize(
    "strategy", [NaivePathAnalysisStrategy, ArticulationSequenceComponentsStrategy]
)
def test_alog_2(strategy: PathAnalysisStrategy):
    G = parse_dot_to_digraph("digraph graphname{\n0->1\n1->2\n2->3\n3->0\n3->4}")
    e1 = "0"
    h = "3"
    analyser = PathAnalyser(strategy)

    assert analyser(G, e1, h) == {"0", "1", "2"}


def test_shortest_path():
    G = path_graph(4, create_using=DiGraph)
    assert ArticulationSequenceComponentsStrategy._find_shortest_path(G, 0, 2) == [
        0,
        1,
        2,
    ]


def test_longer_path():
    G = path_graph(6, create_using=DiGraph)
    assert ArticulationSequenceComponentsStrategy._find_shortest_path(G, 0, 5) == [
        0,
        1,
        2,
        3,
        4,
        5,
    ]


def test_path_with_branch():
    G = DiGraph()
    G.add_edges_from([(0, 1), (1, 2), (2, 5), (5, 3), (1, 4), (4, 3)])
    assert ArticulationSequenceComponentsStrategy._find_shortest_path(G, 0, 3) == [
        0,
        1,
        4,
        3,
    ]


def test_no_path():
    G = path_graph(4, create_using=DiGraph)
    G.remove_edge(2, 3)
    assert ArticulationSequenceComponentsStrategy._find_shortest_path(G, 0, 3) == []


def test_path_with_loop():
    G = DiGraph()
    G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 1), (3, 4)])
    assert ArticulationSequenceComponentsStrategy._find_shortest_path(G, 0, 4) == [
        0,
        1,
        2,
        3,
        4,
    ]


def test_larger_graph():
    G = path_graph(10, create_using=DiGraph)
    assert ArticulationSequenceComponentsStrategy._find_shortest_path(G, 0, 9) == [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
    ]
