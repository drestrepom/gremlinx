# Standar library
from __future__ import annotations
from typing import (
    Union, )

# Third libraries
from networkx import (
    Graph,
    DiGraph,
)
import rx
from rx.core import Observable

# Local imports
from gremlinx.utils.classes import SourceType


class GraphTraversalSource():
    def __init__(
        self,
        graph: Union[Graph, DiGraph],
    ):
        self.graph = graph

    def V(self, *ids: str) -> GraphTraversal:
        """Create a TraversalGraph to traverse the nodes.

        Returns:
            GraphTraversal: nodes.
        """
        return GraphTraversal(
            graph=self.graph,
            sources=rx.of(*ids) if ids else rx.of(
                *list(self.graph.nodes.keys())),
            source_type=SourceType.VERTEX,
        )

    def E(self, *ids: str) -> GraphTraversal:
        """Create a TraversalGraph to traverse the edges.

        Returns:
            GraphTraversal: edges.
        """
        return GraphTraversal(graph=self.graph,
                              sources=rx.of(*ids) if ids else rx.of(
                                  *list(self.graph.edges.keys())),
                              source_type=SourceType.EDGE)


class GraphTraversal():
    def __init__(
        self,
        graph: Union[Graph, DiGraph],
        sources: Observable[str],
        source_type: SourceType,
    ):
        self.graph = graph
        self.sources = sources
        self.source_type = source_type
