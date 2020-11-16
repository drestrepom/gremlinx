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
