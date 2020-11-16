# Standar library
from __future__ import annotations
from typing import (
    Any,
    cast,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)

# Third libraries
from networkx import (
    Graph,
    DiGraph,
)
from networkx.classes.reportviews import (
    NodeView,
    EdgeView,
)
from networkx import subgraph_view

# Local imports
from gremlinx.utils.exceptions import NotExecutable

common_ids_type = Union[str, int]


class GraphTraversal():
    def __init__(
        self,
        graph: Union[Graph, DiGraph],
        nodes: Optional[NodeView] = None,
        edges: Optional[EdgeView] = None,
    ):
        self.graph = graph
        self.nodes = nodes
        self.edges = edges

    def values(self) -> List[Dict[str, Any]]:
        """Simplify access to the results values.

        Raises:
            NotImplementedError: the `TraversalGraph` does not have `nodes` or
            `edges`.

        Returns:
            List[Dict[str, Any]]: return a `List` with the values of the
            `nodes` or `edges`.
        """
        if self.nodes:
            return [data for _, data in self.nodes.nodes().data()]
        if self.edges:
            return [data[2] for data in self.edges.edges().data()]
        raise NotImplementedError

    def data(
        self
    ) -> List[Union[Tuple[common_ids_type, common_ids_type, Dict[str, Any]],
                    Tuple[common_ids_type, Dict[str, Any]]]]:
        """Simplify access to the results data.

        Raises:
            NotImplementedError: the `TraversalGraph` does not have `nodes` or
            `edges`.

        Returns:
            List[Union[Tuple[common_ids_type, common_ids_type, Dict[str, Any]],
            Tuple[common_ids_type, Dict[str, Any]]]]: return a `List` with the
            data of the `nodes` or `edges`.
        """
        if self.nodes:
            return cast(
                List[Union[Tuple[common_ids_type, common_ids_type,
                                 Dict[str, Any]], Tuple[common_ids_type,
                                                        Dict[str, Any]]]],
                self.nodes.nodes.data())
        if self.edges:
            return cast(
                List[Union[Tuple[common_ids_type, common_ids_type,
                                 Dict[str, Any]], Tuple[common_ids_type,
                                                        Dict[str, Any]]]],
                self.edges.edges.data())
        raise NotImplementedError

    def V(self) -> GraphTraversal:
        """Create a TraversalGraph to traverse the nodes.

        Returns:
            GraphTraversal: nodes.
        """
        return GraphTraversal(
            graph=self.graph,
            nodes=self.graph.nodes,
        )

    def E(self) -> GraphTraversal:
        """Create a TraversalGraph to traverse the edges.

        Returns:
            GraphTraversal: edges.
        """
        return GraphTraversal(
            graph=self.graph,
            edges=self.graph,
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
        if not self.nodes:
            raise NotExecutable

        def _has(node: Any) -> bool:
            return any(value == label
                       for key, value in self.graph.nodes[node].items()
                       if key.startswith('label'))

        return GraphTraversal(
            nodes=subgraph_view(
                self.graph,
                filter_node=_has,
            ),
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
            if self.edges:
                raise Exception
        else:
            raise Exception

        def __has(*args: Any, ) -> bool:
            result = None
            if len(args) == 1 and self.nodes:
                result = self.graph.nodes[args[0]].get(
                    prop, None) == value if value else bool(
                        self.graph.nodes[args[0]].get(prop, None))
            if len(args) == 2 and self.edges:
                result = self.graph[args[0]][args[1]].get(
                    prop, None) == value if value else self.graph[args[0]][
                        args[1]].get(prop, None)
            if result is not None:
                return result or negation
            raise NotImplementedError

        result = None
        nodes = self.nodes
        if label:
            result = GraphTraversal(
                nodes=subgraph_view(
                    self.hasLabel(label).nodes,
                    filter_node=__has,
                ),
                graph=self.graph,
            )
            nodes = result.nodes

        if self.nodes:
            result = GraphTraversal(
                nodes=subgraph_view(
                    nodes,
                    filter_node=__has,
                ),
                graph=self.graph,
            )
        if self.edges:
            result = GraphTraversal(
                edges=subgraph_view(
                    self.edges,
                    filter_edge=__has,
                ),
                graph=self.graph,
            )
        if result:
            return result
        raise NotImplementedError

    def has(self, *args: Any) -> GraphTraversal:
        return self._has(*args)

    def hasNot(self, *args: Any) -> GraphTraversal:
        return self._has(*args, negation=True)
