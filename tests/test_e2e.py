from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def test_must_go_through_nodes():
    payload = {
        "e1": "1",
        "h": "5",
        "graph": "digraph graphname{\n1->2\n2->3\n2->5\n5->2\n3->5}",
    }

    response = client.post("/server", json=payload)

    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        "must_go_through_nodes": ["1", "2"]
    } or response.json() == {"must_go_through_nodes": ["2", "1"]}
