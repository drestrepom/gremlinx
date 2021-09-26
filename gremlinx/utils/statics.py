from __future__ import (
    annotations,
)

from gremlinx.utils.classes import (
    GraphTraversalBase,
)
from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
    Union,
)

Vertex = Union[str, Tuple[str, ...], Tuple[Tuple[str, str], ...]]


def hasLabel(
    *labels: str,
    traversal: GraphTraversalBase,
    vertex: Union[str, Tuple[str, str]],
) -> bool:
    if isinstance(vertex, str):
        data = traversal.graph.nodes[vertex]
    else:
        data = traversal.graph[vertex[0]][vertex[1]]
    return all(data.get(f"label_{label}") for label in labels) or all(
        any(
            key.startswith("label") and value == label
            for key, value in data.items()
        )
        for label in labels
    )


def has(
    *args: Any,
    traversal: GraphTraversalBase,
    vertex: Union[str, Tuple[str, str]],
) -> bool:
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
        if traversal.sources_is_edges:
            raise Exception
    else:
        raise Exception
    result = False

    def __has(
        *args: Any,
    ) -> bool:
        _result = False
        if traversal.sources_is_vertex:
            v_id = args[0]
            _result = (
                traversal.graph.nodes[v_id].get(prop) == value
                if value
                else bool(traversal.graph.nodes[v_id].get(prop))
            )

        elif traversal.sources_is_edges:
            v_out, v_in = args
            _result = (
                traversal.graph[v_out][v_in].get(prop) == value
                if value
                else bool(traversal.graph[v_out][v_in].get(prop))
            )

        return _result

    if label:
        result = hasLabel(label, traversal=traversal, vertex=vertex)

    if traversal.sources_is_vertex and value and label:
        result = result and __has(vertex)
    elif traversal.sources_is_vertex:
        result = __has(vertex)
    elif traversal.sources_is_edges:
        result = __has(*vertex)
    return result


def out(
    *labels: Any,
    traversal: GraphTraversalBase,
    vertex: Vertex,
) -> Tuple[str, ...]:
    # in this case vertex is the complete path
    _vertex = vertex[-1]
    childs: Tuple[str, ...] = tuple(traversal.graph.adj[_vertex])
    return tuple(
        (*vertex, child)
        for child in childs
        if (
            all(
                hasLabel(label, vertex=(_vertex, child), traversal=traversal)
                for label in labels
            )
            if labels
            else True
        )
    )


def In(
    *labels: Any,
    traversal: GraphTraversalBase,
    vertex: Vertex,
) -> Tuple[str, ...]:
    # in this case vertex is the complete path
    _vertex = vertex[-1]
    parents = tuple(traversal.graph.pred[_vertex])

    return tuple(
        (*vertex, parent)
        for parent in parents
        if (
            all(
                hasLabel(label, vertex=(_vertex, parent), traversal=traversal)
                for label in labels
            )
            if labels
            else True
        )
    )


def values(
    *propertis: Any,
    traversal: GraphTraversalBase,
    vertex: Union[str, Tuple[str, str]],
) -> Union[Any, Dict[str, Any]]:
    if traversal.sources_is_edges:
        _out, ingress = vertex  # type: ignore
        source = traversal.graph[_out][ingress]
    else:
        source = traversal.graph.nodes[vertex]
    if propertis:
        source = {
            key: value for key, value in source.items() if key in propertis
        }
    return source


def fold(
    *,
    vertex: Union[str, Tuple[str, str]],
) -> Union[Any, Dict[str, Any]]:
    if isinstance(vertex, dict):
        _values = tuple(vertex.values())
        if len(_values) == 1:
            return _values[0]
        return _values

    return vertex
