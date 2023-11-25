import logging
from parser import parse_dot_to_digraph

import networkx as nx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from algo import PathAnalyser

app = FastAPI()

# setup logging
logger = logging.getLogger(__name__)


class PathAnalysisRequestDTO(BaseModel):
    graph: str
    e1: str
    h: str


def find_must_go_through_nodes(G: nx.DiGraph, e1: str, h: str) -> set[str]:
    algo = PathAnalyser()
    return algo(G, e1, h)


@app.post("/server")
def process_graph(input: PathAnalysisRequestDTO):
    try:
        G = parse_dot_to_digraph(input.graph)
        nodes = find_must_go_through_nodes(G, input.e1, input.h)
        return {
            "must_go_through_nodes": list(nodes)
        }  # We might want in the future to return more parameters
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
