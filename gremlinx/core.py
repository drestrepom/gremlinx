# Standar library
from __future__ import annotations
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Tuple,
    Union,
)

# Third libraries
from networkx import (
    Graph,
    DiGraph,
)
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
        self.__results__: List[str] = []

    def __iter__(self) -> GraphTraversal:
        self.sources.subscribe(self.__results__.append)
        return self

    def __next__(self) -> Union[str, Tuple[str, str]]:
        try:
            return self.__results__.pop()
        except IndexError:
            raise StopIteration

    @property
    def sources_is_vertex(self) -> bool:
        return self.source_type == SourceType.VERTEX

    @property
    def sources_is_edges(self) -> bool:
        return self.source_type == SourceType.EDGE

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

        self.sources = self.sources.pipe(
            ops.filter(lambda x: statics.hasLabel(
                *labels,
                traversal=self,
                vertex=x,
            )))
        return self

    def has(self, *args: Any) -> GraphTraversal:
        self.sources = self.sources.pipe(
            ops.filter(lambda x: statics.has(
                *args,
                traversal=self,
                vertex=x,
            )))
        return self

    def hasNot(self, *args: Any) -> GraphTraversal:
        self.sources = self.sources.pipe(
            ops.filter(lambda x: not statics.has(
                *args,
                traversal=self,
                vertex=x,
            )))
        return self

    def Not(
        self, function: Tuple[Callable[[Any], bool], Tuple[Any, ...],
                              Dict[str, Any]]
    ) -> GraphTraversal:
        _function, args, kwargs = function
        self.sources = self.sources.pipe(
            ops.filter(lambda x: not _function(  # type: ignore
                traversal=self, vertex=x, *args, **kwargs)))
        return self

    def out(self, *labels: str) -> GraphTraversal:
        if self.sources_is_edges:
            raise NotExecutable
        self.sources = self.sources.pipe(
            ops.flat_map(lambda x: rx.of(*statics.out(
                *labels,
                vertex=x,
                traversal=self,
            ))))
        return self

    def values(
        self,
        *properties: str,
    ) -> GraphTraversal:
        """Simplify access to the results values.

        Raises:
            NotImplementedError: the `TraversalGraph` does not have `nodes` or
            `edges`.

        Returns:
            List[Dict[str, Any]]: return a `List` with the values of the
            `nodes` or `edges`.
        """
        self.sources = self.sources.pipe(
            ops.map(lambda x: statics.values(
                *properties,
                traversal=self,
                vertex=x,
            )))
        return self
