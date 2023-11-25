import logging

import networkx as nx

logger = logging.getLogger(__name__)


class PathAnalyser:
    def __call__(self, G: nx.DiGraph, e1: str, h: str) -> set[str]:
        self._validate_input(G, e1, h)
        return self._naive_solution(G, e1, h)

    def _validate_input(self, G: nx.DiGraph, e1: str, h: str) -> None:
        """Validate the input to the path analysis."""

        if not G.has_node(e1):
            msg = f"{e1!r} is not a node in the graph"
            raise ValueError(msg)
        if not G.has_node(h):
            msg = f"{h!r} is not a node in the graph"
            raise ValueError(msg)

    def _naive_solution(self, G: nx.DiGraph, e1: str, h: str) -> set[str]:
        """
        A naive solution to the path analysis problem.
        :param G: The graph to search for articulation points.
        :param e1: The start node.
        :param h: The end node.
        :return: A set of moust-go-through nodes.
        """

        def dfs(G: nx.DiGraph, start, path, all_paths):
            path = path + [start]
            if start == h:
                all_paths.append(path)
            else:
                for node in G.neighbors(start):
                    if (
                        node not in path
                    ):  # Can switch to defultdict(bool) to lower complexity
                        dfs(G, node, path, all_paths)

        all_paths: list[list] = []
        dfs(G, e1, [], all_paths)

        if not all_paths:
            raise ValueError(f"No path from {e1!r} to {h!r}")

        must_go_through = set(all_paths[0])
        for path in all_paths[1:]:
            must_go_through.intersection_update(path)

        must_go_through.remove(h)
        return must_go_through
