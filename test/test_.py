# Third libraries
import networkx as nx

# Local imports
from gremlinx.core import GraphTraversalSource
from gremlinx.statics import hasLabel


def test_v(source: GraphTraversalSource) -> None:
    vertexes = list(source.V())
    assert len(vertexes) == 3619


def test_e(source: GraphTraversalSource) -> None:
    vertexes = list(source.E())
    assert len(vertexes) == 50148


def test_has_label(source: GraphTraversalSource) -> None:
    airports = list(source.V().hasLabel('airport'))
    assert len(airports) == 3374
    assert '8' in airports


def test_has(source: GraphTraversalSource) -> None:
    airport = list(source.V().has('code', 'DFW'))
    assert len(airport) == 1
    assert '8' in airport


def test_not(source: GraphTraversalSource) -> None:
    no_airports = list(source.V().Not(hasLabel('airport')))
    assert len(no_airports) == 245
    assert '0' in no_airports
    assert '1' not in no_airports

def test_out(source: GraphTraversalSource) -> None:
    dest = list(source.V().has('airport','code','AUS').out())
    assert len(dest) == 59
