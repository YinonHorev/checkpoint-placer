from collections import defaultdict
import logging
from typing_extensions import DefaultDict

import networkx as nx

from api import PathAnalysisRequest


logger = logging.getLogger(__name__)

class PathAnalyser:
    def __call__(self, G: nx.DiGraph, e1: str, h: str) -> set[str]:
        self._validate_input(G, e1, h)
        self.visited = defaultdict(bool)
        self.depth = defaultdict(int)
        self.low = defaultdict(int)
        self.result = set()
        self.h_found = False
        self._articulation_points(G, e1, h, 0)
        if not self.h_found:
            msg = f"{h!r} is not reachable from {e1!r}"
            logger.error(msg)
            raise ValueError(msg)
        return self.result


    def _validate_input(self, G: nx.DiGraph, e1: str, h: str) -> None:
        """Validate the input to the path analysis."""

        if not G.has_node(e1):
            msg = f"{e1!r} is not a node in the graph"
            logger.error(msg)
            raise ValueError(msg)
        if not G.has_node(h):
            msg = f"{h!r} is not a node in the graph"
            logger.error(msg)
            raise ValueError(msg)


    def _articulation_points(self, G: nx.Graph, s: str, h: str, d: int) -> None:
        """
        Find articulation points in a graph.
        :param G: The graph to search for articulation points.
        :return: A set of articulation points.
        """
        self.visited[s] = True
        self.depth[s] = d
        self.low[s] = d
        if s == h: # Probably not needed since CFG ensures that h is reachable from e1
            self.h_found = True
            return
        for k in G.neighbors(s):
            if not self.visited[k]:
                self._articulation_points(G, k, h, d + 1)
            self.low[s] = min(self.low[s], self.low[k])
            if self.low[k] >= self.depth[s] and k != h:
                self.result.add(s)
