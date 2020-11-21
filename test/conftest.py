# Standard library
from typing import Iterator

# Third party libraries
import pytest
from networkx import DiGraph
import networkx as nx

# Local imports
from gremlinx.core import GraphTraversalSource

TEST_GRAPH: DiGraph = nx.read_graphml('test/data/air-routes.graphml')


@pytest.fixture(scope='session')
def source() -> Iterator[GraphTraversalSource]:
    yield GraphTraversalSource(graph=TEST_GRAPH)
