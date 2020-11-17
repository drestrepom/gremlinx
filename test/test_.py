from networkx import DiGraph
import networkx as nx
from gremlinx import GraphTraversal

def test_out_1(test_traversal: GraphTraversal) -> None:
    expected = set([
        'PDX',
        'CLT',
        'ATL',
        'AUS',
        'BOS',
        'BWI',
        'DFW',
        'IAD',
        'IAH',
        'JFK',
        'LAX',
        'MIA',
        'MSP',
        'ORD',
        'PHX',
        'RDU',
        'SEA',
        'SFO',
        'SJC',
        'SAN',
        'SLC',
        'LAS',
        'DEN',
        'MSY',
        'EWR',
        'PHL',
        'DTW',
    ])
    result = set(test_traversal.V().has('code',
                           'LHR').out('route').has('country',
                                                   'US').values('code'))
    assert expected == result
