from gremlinx.core import (
    GraphTraversalSource,
)
import networkx as nx
from networkx import (
    DiGraph,
)
import pytest
from typing import (
    Iterator,
)

TEST_GRAPH: DiGraph = nx.read_graphml("test/data/air-routes.graphml")


@pytest.fixture(scope="session")
def source() -> Iterator[GraphTraversalSource]:
    yield GraphTraversalSource(graph=TEST_GRAPH)
