# pylint: disable=invalid-name
from __future__ import (
    annotations,
)

from collections import (
    UserDict,
)
from contextlib import (
    suppress,
)
from gremlinx.utils import (
    statics,
)
from gremlinx.utils.classes import (
    GraphTraversalBase,
    SourceType,
)
from gremlinx.utils.exceptions import (
    NotExecutable,
)
from networkx import (
    DiGraph,
    Graph,
)
from networkx.utils.misc import (
    iterable,
)
import rx
from rx.core import (
    Observable,
)
import rx.operators as ops
from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    Tuple,
    Union,
)


class GraphTraversalSource:
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
            sources=rx.of(*((_vertex,) for _vertex in ids))
            if ids
            else rx.of(*((_vertex,) for _vertex in self.graph.nodes.keys())),
            source_type=SourceType.VERTEX,
        )

    def E(self, *ids: str) -> GraphTraversal:
        """Create a TraversalGraph to traverse the edges.

        Returns:
            GraphTraversal: edges.
        """
        return GraphTraversal(
            graph=self.graph,
            sources=rx.of(*((_edge,) for _edge in ids))
            if ids
            else rx.of(*((_edge,) for _edge in self.graph.edges.keys())),
            source_type=SourceType.EDGE,
        )


class GraphTraversal(GraphTraversalBase):
    def __init__(
        self,
        graph: Union[Graph, DiGraph],
        sources: Observable[str],
        source_type: SourceType,
    ):
        super().__init__(graph, sources, source_type)
        self.is_path = False

    def __iter__(self) -> GraphTraversal:
        self.sources.subscribe(self.__results__.append)
        return self

    def __next__(self) -> Union[str, Tuple[str, str]]:
        try:
            _next = self.__results__.pop()
            if self.is_path:
                return _next
            try:
                return _next[-1]
            except KeyError:
                return _next
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
        self.sources = self.sources.pipe(
            ops.filter(
                lambda x: statics.hasLabel(
                    *labels, traversal=self, vertex=x[-1]
                )
            )
        )
        return self

    def has(self, *args: Any) -> GraphTraversal:
        self.sources = self.sources.pipe(
            ops.filter(
                lambda x: statics.has(*args, traversal=self, vertex=x[-1])
            )
        )
        return self

    def hasNot(self, *args: Any) -> GraphTraversal:
        self.sources = self.sources.pipe(
            ops.filter(
                lambda x: not statics.has(*args, traversal=self, vertex=x[-1])
            )
        )
        return self

    def Not(
        self,
        function: Tuple[
            Callable[[Any], bool], Tuple[Any, ...], Dict[str, Any]
        ],
    ) -> GraphTraversal:
        _function, args, kwargs = function
        self.sources = self.sources.pipe(
            ops.filter(
                lambda x: not _function(  # type: ignore
                    traversal=self, vertex=x[-1], *args, **kwargs
                )
            )
        )
        return self

    def out(self, *labels: str) -> GraphTraversal:
        if self.sources_is_edges:
            raise NotExecutable
        self.sources = self.sources.pipe(
            ops.flat_map(
                lambda x: rx.of(
                    *statics.out(*labels, vertex=x, traversal=self)
                )
            )
        )
        return self

    def outE(self, *labels: str) -> GraphTraversal:
        return self.out(*labels)

    def In(self, *labels: str) -> GraphTraversal:
        if self.sources_is_edges:
            raise NotExecutable
        self.sources = self.sources.pipe(
            ops.flat_map(
                lambda x: rx.of(*statics.In(*labels, vertex=x, traversal=self))
            )
        )
        return self

    def inV(self, *labels: str) -> GraphTraversal:
        return self.In(*labels)

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
            ops.map(
                lambda x: statics.values(
                    *properties, traversal=self, vertex=x[-1]
                )
            )
        )
        return self

    def fold(self) -> GraphTraversal:
        self.sources = self.sources.pipe(
            ops.map(lambda x: statics.fold(vertex=x[-1]))
        )
        return self

    def count(self) -> int:
        return len(tuple(self))

    def path(self) -> GraphTraversal:
        self.is_path = True
        return self

    def group(self) -> GraphGroup:
        return GraphGroup(self)

    def groupCount(self) -> GraphGroupCount:
        return GraphGroupCount(self)


class GraphGroup(UserDict):
    def __init__(
        self, graph_traversal: Optional[GraphTraversal] = None, **kwargs: Any
    ) -> None:
        self.graph_traversal = graph_traversal
        new_dict = {n_id: n_id for n_id in graph_traversal}
        super().__init__(kwargs or new_dict)

    def by(
        self, transformer: Callable[[GraphGroup], Dict[Any, Any]]
    ) -> GraphGroup:
        self.__init__(
            graph_traversal=self.graph_traversal, **transformer(self)
        )
        return self


class GraphGroupCount(UserDict):
    def __init__(
        self, graph_traversal: Optional[GraphTraversal] = None, **kwargs: Any
    ) -> None:
        self.graph_traversal = graph_traversal

        new_dict = {}
        if not kwargs:
            for element in self.graph_traversal:
                if element in new_dict:
                    new_dict[element] += 1
                else:
                    new_dict[element] = 1

        for key, value in kwargs.items():
            if iterable(value):
                kwargs[key] = len(value)

        super().__init__(kwargs or new_dict)

    def _by_edges(
        self,
        transformer: Union[str, Callable[[GraphGroupCount], Dict[Any, Any]]],
    ) -> GraphGroupCount:
        if isinstance(transformer, str):
            new_dict: Dict[Any, int] = {}
            for out_edge, in_edge in self.graph_traversal:
                with suppress(KeyError):
                    property_value = self.graph_traversal.graph.edges[
                        out_edge
                    ][in_edge].get(transformer)
                    if property_value and property_value in new_dict:
                        new_dict[property_value] += 1
                    elif property_value:
                        new_dict[property_value] = 1

            self.__init__(graph_traversal=self.graph_traversal, **new_dict)
            return self
        return self

    def _by_vertex(
        self,
        transformer: Union[str, Callable[[GraphGroupCount], Dict[Any, Any]]],
    ):
        if isinstance(transformer, str):
            new_dict: Dict[Any, int] = {}
            for n_id in self.graph_traversal:
                property_value = self.graph_traversal.graph.nodes[n_id].get(
                    transformer
                )
                if property_value and property_value in new_dict:
                    new_dict[property_value] += 1
                elif property_value:
                    new_dict[property_value] = 1

            self.__init__(graph_traversal=self.graph_traversal, **new_dict)
            return self
        return self

    def by(
        self,
        transformer: Union[str, Callable[[GraphGroupCount], Dict[Any, Any]]],
    ) -> GraphGroupCount:
        if callable(transformer):
            self.__init__(
                graph_traversal=self.graph_traversal, **transformer(self)
            )
            return self
        if self.graph_traversal.sources_is_vextex():
            return self._by_vertex(transformer)
        if self.graph_traversal.sources_is_edge():
            return self._by_edges(transformer)
        return self
