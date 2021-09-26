from enum import (
    Enum,
)
from networkx.classes.digraph import (
    DiGraph,
)
from networkx.classes.graph import (
    Graph,
)
from rx.core.typing import (
    Observable,
)
from typing import (
    List,
    Tuple,
    Union,
)


class SourceType(Enum):
    VERTEX = "Vertex"
    EDGE = "EDGE"


class GraphTraversalBase:
    def __init__(
        self,
        graph: Union[Graph, DiGraph],
        sources: Observable[Tuple[str, ...]],
        source_type: SourceType,
    ):
        self.graph = graph
        self.sources = sources
        self.source_type = source_type
        self.__results__: List[str] = []
