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
        if self.nodes:
            return [data for _, data in self.nodes.nodes.data()]
        raise Exception

    def data(self) -> List[Tuple[str, Dict[str, Any]]]:
        if self.nodes:
            return cast(List[Tuple[str, Dict[str, Any]]],
                        self.nodes.nodes.data())
        raise Exception

    def V(self) -> GraphTraversal:
        return GraphTraversal(
            graph=self.graph,
            nodes=self.graph.nodes,
        )

    def E(self) -> GraphTraversal:
        return GraphTraversal(
            graph=self.graph,
            edges=self.graph.edges,
        )

    def hasLabel(self, label: str) -> GraphTraversal:
        if not self.nodes:
            raise NotImplementedError

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
        value: Any = True

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
                result = self.graph.nodes[args[0]].get(prop, None) == value
            if len(args) == 2 and self.edges:
                result = self.graph[args[0]][args[1]].get(prop, None) == value
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
