<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
# Contents

- [gremlinx](#gremlinx)
    - [Getting start](#getting-start)
        - [Basic Gremlimx queries](#basic-gremlimx-queries)
        - [Retrieving property values from a vertex](#retrieving-property-values-from-a-vertex)
        - [Does a specific property exist on a given vertex or edge?](#does-a-specific-property-exist-on-a-given-vertex-or-edge)
        - [Counting things](#counting-things)
        - [Counting groups of things](#counting-groups-of-things)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# gremlinx

GremlinX is an attempt to implement the gremlin language on networkx.

## Getting start

Load a dataset of air routes
Load a dataset of air routes

```python
from gremlinx.core import (
    GraphTraversalSource,
)
import networkx as nx

G = nx.read_graphml("test/data/air-routes.graphml")
g = GraphTraversalSource(graph=G)
```

### Basic Gremlimx queries

The query below will return any vertices (nodes) that have the airport label.

```python
# Find vertices that are airports
g.V().hasLabel('airport')
```

This query will return the vertex that represents the Dallas Fort Worth (DFW) airport.

```python
# Find the DFW vertex
g.V().has('code','DFW')
```

The next two queries combine the previous two into a single query.

```python
# Combining those two previous queries (two ways that are equivalent)
g.V().hasLabel('airport').has('code','DFW')

g.V().has('airport','code','DFW')
```

### Retrieving property values from a vertex

```python
# What property values are stored in the DFW vertex?
g.V().has('airport','code','DFW').values()
```

The values step can take parameters that tell it to only return the values for
the provided key names.

```python
g.V().has('airport','code','DFW').values('city')

g.V().has('airport','code','DFW').values('runways','icao')
```

### Does a specific property exist on a given vertex or edge?

You can simply test to see if a property exists as well as testing for it
containing a specific value.

```python
# Find all edges that have a 'dist' property
g.E().has('dist')

# Find all vertices that have a 'region' property
g.V().has('region')

# Find all the vertices that do not have a 'region' property
g.V().hasNot('region')

# The above is shorthand for
 g.V().not(has('region'))
```

### Counting things

```python
# How many airports are there in the graph?
g.V().hasLabel('airport').count()

# How many routes are there?
g.V().hasLabel('airport').outE('route').count()

# How many routes are there?
g.V().outE('route').count()

# How many routes are there?
g.E().hasLabel('route').count()
```

### Counting groups of things

```python
# How many of each type of vertex are there?
g.V().groupCount().by(label)
```

We can also run a similar query to find out the distribution of edge labels in the graph

```python
# How many of each type of edge are there?
g.E().groupCount().by(label)
```

By way of a side note, the examples above are shorthand ways of writing something like this example which also counts vertices by label.

```python
# As above but using group()
g.V().group().by(label).by(count())
```

```python
# How many airports are there in each country?
g.V().hasLabel('airport').groupCount().by('country')
```
