from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from queue import SimpleQueue

import networkx as nx


@dataclass
class Path:
    Nodes: list[str]
    Edges: list[tuple[str, str]]


class PathAnalysisStrategy(ABC):
    @staticmethod
    @abstractmethod
    def analyse_path(G: nx.DiGraph, e1: str, h: str) -> set[str]:
        pass


class NaivePathAnalysisStrategy(PathAnalysisStrategy):
    @staticmethod
    def analyse_path(G: nx.DiGraph, e1: str, h: str) -> set[str]:
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


class ArticulationSequenceComponentsStrategy(PathAnalysisStrategy):
    @staticmethod
    def analyse_path(G: nx.DiGraph, e1: str, h: str) -> set[str]:
        # Step 1: Find an arbitrary e1-h path in G
        P = nx.shortest_path(
            G, source=e1, target=h
        )  # Using shortest path for simplicity
        P = Path(P, [(u, v) for u, v in zip(P, P[1:])])
        P_reversed = Path(P.Nodes[::-1].copy(), [(v, u) for (u, v) in P.Edges[::-1]])
        # Step 2: Graph Transformation
        G = G.copy()
        # G.add_edges_from([e for e in P_reversed.Edges if e not in G.edges])  # Adding P^-1
        G.add_edges_from(P_reversed.Edges)  # Adding P^-1
        out = defaultdict(int)
        for u in G.nodes:
            if u in P.Nodes[1:-1]:
                out[u] = 0
            else:
                out[u] = 1

        # Step 3: Find articulation points and components
        comp: dict[str, int] = defaultdict(int)
        Q: SimpleQueue = SimpleQueue()
        A, i = set(), 1
        while comp[h] == 0:
            if i == 1:
                Q.put_nowait(e1)
                comp[e1] = 1
            else:
                for i, u in enumerate(P.Nodes):
                    if comp[u] == 0:
                        break
                y = P.Nodes[i - 1]
                A.add(y)
                out[y] = 1
                Q.put_nowait(y)
                comp[y] = i

            while not Q.empty():
                u = Q.get_nowait()
                for v in G.neighbors(u):
                    if out[u] == 1 or ((u, v) in P_reversed.Edges):
                        if comp[v] == 0 or ((u, v) in P_reversed.Edges and out[v] == 0):
                            Q.put_nowait(v)
                            comp[v] = i
                            if (v, u) in P.Edges:
                                out[v] = 1
            i += 1
        A.add(e1)
        return A
