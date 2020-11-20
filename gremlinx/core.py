# Standar library
from __future__ import annotations
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Generator,
    Optional,
    Tuple,
    Union,
)
from enum import Enum

# Third libraries
from networkx import (
    Graph,
    DiGraph,
    dfs_successors,
)
import networkx as nx
import rx
from rx.core import Observable
import rx.operators as ops

# Local imports
from gremlinx.utils.exceptions import NotExecutable
from gremlinx.utils.classes import SourceType
from gremlinx.utils import statics


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

    @property
    def sources_is_vertex(self) -> bool:
        return self.source_type == SourceType.VERTEX

    @property
    def sources_is_edges(self) -> bool:
        return self.source_type == SourceType.EDGE

    def _has_label(self, vertex: str, *labels: str) -> bool:
        vertex_data = self.graph.nodes[vertex]
        return all(vertex_data.get(f'label_{label}')
                   for label in labels) or all(
                       any(
                           key.startswith('label') and value == label
                           for key, value in vertex_data.items())
                       for label in labels)

    def hasLabel(self, *labels: str) -> GraphTraversal:
        """Filter the nodes that have the label.

        Networkx does not have native support for labels, they must be,
        simulated with node properties.

        To filter the nodes by labels, the labels must have the following
        format.

        >>> G.addNode('1', labelV='airport')

        The key of the label must have the following format `label[anything]`.
        >>> # Find nodes that are airports
        >>> g.V().hasLabel('airport')

        Args:
            labels (*str): labels values.

        Raises:
            NotExecutable: this function can only be executed on nodes.

        Returns:
            GraphTraversal: nodes that contain the indicated label.
        """
        if self.source_type == SourceType.EDGE:
            raise NotExecutable

        return GraphTraversal(
            sources=self.sources.pipe(
                ops.filter(lambda x: statics.hasLabel(self, x, *labels))),
            graph=self.graph,
            source_type=self.source_type,
        )
