# Standard library
from typing import Iterator

# Third party libraries
import pytest
from networkx import DiGraph
import networkx as nx

# Local imports
from gremlinx import GraphTraversal

TEST_GRAPH: DiGraph = nx.read_graphml('test/data/air-routes.graphml')


@pytest.fixture(scope='session')
def test_traversal() -> Iterator[GraphTraversal]:
    yield GraphTraversal(graph=TEST_GRAPH)
