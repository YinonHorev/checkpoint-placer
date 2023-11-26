import logging

import networkx as nx

from strategy import PathAnalysisStrategy

logger = logging.getLogger(__name__)


class PathAnalyser:
    def __init__(self, strategy: PathAnalysisStrategy) -> None:
        self.strategy = strategy

    def __call__(self, G: nx.DiGraph, e1: str, h: str) -> set[str]:
        self._validate_input(G, e1, h)
        return self.strategy.analyse_path(G, e1, h)

    def _validate_input(self, G: nx.DiGraph, e1: str, h: str) -> None:
        """Validate the input to the path analysis."""

        if not G.has_node(e1):
            msg = f"{e1!r} is not a node in the graph"
            raise ValueError(msg)
        if not G.has_node(h):
            msg = f"{h!r} is not a node in the graph"
            raise ValueError(msg)

    import networkx as nx
