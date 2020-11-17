# Standar library
from __future__ import annotations
from typing import (
    Any,
    Dict,
    List,
    Generator,
    Optional,
    Tuple,
    Union,
)

# Third libraries
from networkx import (
    Graph,
    DiGraph,
)
from networkx import subgraph_view

# Local imports
from gremlinx.utils.exceptions import NotExecutable

common_ids_type = Union[str, int]


class GraphTraversal():
    def __init__(
        self,
        graph: Union[Graph, DiGraph],
        sources: Optional[List[Union[common_ids_type,
                                     Tuple[common_ids_type,
                                           common_ids_type]]]] = None,
    ):
        self.graph = graph
        self.sources = sources or list()

    def _sources_is_nodes(self) -> bool:
        if self.sources:
            return not isinstance(self.sources[0], tuple)
        return False

    def _sources_is_edges(self) -> bool:
        if self.sources:
            return isinstance(self.sources[0], tuple)
        return False

    def values(self) -> Generator[Dict[str, Any], None, None]:
        """Simplify access to the results values.

        Raises:
            NotImplementedError: the `TraversalGraph` does not have `nodes` or
            `edges`.

        Returns:
            List[Dict[str, Any]]: return a `List` with the values of the
            `nodes` or `edges`.
        """
        for item in self.sources:
            if self._sources_is_edges():
                out, ingress = item  # type: ignore
                yield self.graph[out][ingress]
            else:
                yield self.graph.nodes[item]

    def data(
        self
    ) -> Generator[Union[Tuple[common_ids_type, common_ids_type, Dict[
            str, Any]], Tuple[common_ids_type, Dict[str, Any]]], None, None]:
        """Simplify access to the results data.

        Raises:
            NotImplementedError: the `TraversalGraph` does not have `nodes` or
            `edges`.

        Returns:
            List[Union[Tuple[common_ids_type, common_ids_type, Dict[str, Any]],
            Tuple[common_ids_type, Dict[str, Any]]]]: return a `List` with the
            data of the `nodes` or `edges`.
        """
        for item in self.sources:
            if self._sources_is_edges():
                out, ingress = item  # type: ignore
                yield (out, ingress, self.graph[out][ingress])
            else:
                yield self.graph.nodes[item]

    def V(self) -> GraphTraversal:
        """Create a TraversalGraph to traverse the nodes.

        Returns:
            GraphTraversal: nodes.
        """
        return GraphTraversal(
            graph=self.graph,
            sources=list(self.graph.nodes.keys()),
        )

    def E(self) -> GraphTraversal:
        """Create a TraversalGraph to traverse the edges.

        Returns:
            GraphTraversal: edges.
        """
        return GraphTraversal(
            graph=self.graph,
            sources=list(self.graph.edges.keys()),
        )

    def hasLabel(self, label: str) -> GraphTraversal:
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
            label (str): value of label.

        Raises:
            NotExecutable: this function can only be executed on nodes

        Returns:
            GraphTraversal: nodes that contain the indicated label.
        """
        if self._sources_is_edges():
            raise NotExecutable

        def _has(node: common_ids_type) -> bool:
            if node in self.sources:
                return any(value == label
                           for key, value in self.graph.nodes[node].items()
                           if key.startswith('label'))
            return False

        return GraphTraversal(
            sources=list(
                subgraph_view(
                    self.graph,
                    filter_node=_has,
                ).nodes.keys()),
            graph=self.graph,
        )

    def _has(
        self,
        *args: Any,
        negation: bool = False,
    ) -> GraphTraversal:
        label: Optional[str] = None
        prop: Optional[str] = None
        value: Optional[Any] = None

        if len(args) == 1:
            prop = args[0]
        elif len(args) == 2:
            prop = args[0]
            value = args[1]
        elif len(args) == 3:
            label = args[0]
            prop = args[1]
            value = args[2]
            if self._sources_is_edges():
                raise Exception
        else:
            raise Exception

        result: Optional[GraphTraversal] = None

        def __has(*args: Any, ) -> bool:
            _result = None
            if result and self._sources_is_nodes(
            ) and args[0] not in result.sources:
                return False

            if self._sources_is_nodes and args[0] in self.sources:
                _result = self.graph.nodes[args[0]].get(
                    prop, None) == value if value else bool(
                        self.graph.nodes[args[0]].get(prop, None))
            elif self._sources_is_edges() and args in self.sources:
                _result = self.graph[args[0]][args[1]].get(
                    prop, None) == value if value else self.graph[args[0]][
                        args[1]].get(prop, None)
            if _result is not None:
                return _result or negation
            raise NotImplementedError

        if label:
            result = GraphTraversal(
                sources=list(
                    subgraph_view(
                        self.graph,
                        filter_node=__has,
                    ).nodes.keys()),
                graph=self.graph,
            )

        if self._sources_is_nodes():
            result = GraphTraversal(
                sources=list(
                    subgraph_view(
                        self.graph,
                        filter_node=__has,
                    ).nodes.keys()),
                graph=self.graph,
            )
        elif self._sources_is_edges():
            result = GraphTraversal(
                sources=list(
                    subgraph_view(
                        self.graph,
                        filter_edge=__has,
                    ).edges.keys()),
                graph=self.graph,
            )
        if result:
            return result
        raise NotImplementedError

    def has(self, *args: Any) -> GraphTraversal:
        return self._has(*args)

    def hasNot(self, *args: Any) -> GraphTraversal:
        return self._has(*args, negation=True)
