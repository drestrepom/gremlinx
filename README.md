# gremlinx

Gremlin X is an attempt to implement the gremlin language on networkx.

# Getting start
Load a dataset of air routes
```python
from gremlinx.core import (
    GraphTraversalSource,
)
import networkx as nx

G = nx.read_graphml("test/data/air-routes.graphml")
T = GraphTraversalSource(graph=G)
# get the airports with the code DFW
T.V().has('code', 'DFW')

# get all available routes from Austin airport
T.V().has("airport", "code", "AUS").out()

# get all vertex that are not airports
T.V().Not(hasLabel("airport"))
 ```
