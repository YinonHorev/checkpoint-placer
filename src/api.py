import logging
from parser import parse_dot_to_digraph

import networkx as nx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# setup logging
logging.basicConfig(level=logging.INFO)


class PathAnalysisRequest(BaseModel):
    graph: str
    e1: str
    h: str


def find_must_go_through_nodes(G: nx.DiGraph, e1: str, h: str) -> set[int]:
    return {1, 2}  # Currently a stub for testing


@app.post("/server")
def process_graph(input: PathAnalysisRequest):
    try:
        G = parse_dot_to_digraph(input.graph)
        nodes = find_must_go_through_nodes(G, input.e1, input.h)
        return {
            "must_go_through_nodes": list(nodes)
        }  # We might want in the future to return more parameters
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
