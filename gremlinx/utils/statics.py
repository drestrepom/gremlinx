# Standar library
from __future__ import annotations
from typing import (
    Any,
    Optional,
    Tuple,
    Union,
)

# Third libraries

# Local imports


def hasLabel(traversal: Any, vertex: Union[str, Tuple[str, str]],
             *labels: str) -> bool:
    vertex_data = traversal.graph.nodes[vertex]
    return all(vertex_data.get(f'label_{label}') for label in labels) or all(
        any(
            key.startswith('label') and value == label
            for key, value in vertex_data.items()) for label in labels)


def has(
    *args: Any,
    traversal: Any,
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

    def __has(*args: Any, ) -> bool:
        _result = False
        if traversal.sources_is_vertex:
            v_id = args[0]
            _result = traversal.graph.nodes[v_id].get(
                prop) == value if value else bool(
                    traversal.graph.nodes[v_id].get(prop))

        elif traversal.sources_is_edges:
            v_out, v_in = args
            _result = traversal.graph[v_out][v_in].get(
                prop) == value if value else bool(
                    traversal.graph[v_out][v_in].get(prop))

        return _result

    if label:
        result = hasLabel(traversal, vertex, label)

    if traversal.sources_is_vertex and value:
        result = result and __has(vertex)
    elif traversal.sources_is_vertex:
        result = __has(vertex)
    elif traversal.sources_is_edges:
        result = __has(*vertex)
    return result
