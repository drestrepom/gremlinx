from gremlinx.core import (
    GraphGroup,
)
from gremlinx.utils.statics import (
    has as _has,
    hasLabel as _hasLabel,
)
from mypy_extensions import (
    NamedArg,
    VarArg,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Tuple,
    Union,
)


def has(
    *args: str,
) -> Tuple[
    Callable[
        [
            VarArg(Any),
            NamedArg(Any, "traversal"),
            NamedArg(Union[str, Tuple[str, str]], "vertex"),
        ],
        bool,
    ],
    Tuple[str, ...],
    None,
]:
    return _has, args, dict()


def hasLabel(
    *labels: str,
) -> Tuple[
    Callable[
        [
            VarArg(Any),
            NamedArg(Any, "traversal"),
            NamedArg(Union[str, Tuple[str, str]], "vertex"),
        ],
        bool,
    ],
    Tuple[str, ...],
    None,
]:
    return _hasLabel, labels, dict()


def label(group: GraphGroup) -> Dict[str, str]:
    new_dict: Dict[Any, List[Any]] = {}
    if group.graph_traversal.sources_is_vextex():
        for n_id in group.graph_traversal:
            label_name = group.graph_traversal.graph.nodes[n_id].get("labelV")
            if label_name and label_name in new_dict:
                new_dict[label_name].append(n_id)
            elif label_name:
                new_dict[label_name] = [n_id]
    elif group.graph_traversal.sources_is_edge():
        for out_edge, in_edge in group.graph_traversal:
            label_name = group.graph_traversal.graph[out_edge][in_edge].get(
                "labelE"
            )
            if label_name and label_name in new_dict:
                new_dict[label_name].append(f"{out_edge}-{in_edge}")
            elif label_name:
                new_dict[label_name] = [f"{out_edge}-{in_edge}"]
    return new_dict


def count() -> Callable[[GraphGroup], GraphGroup]:
    def transformer(group: GraphGroup) -> GraphGroup:
        for key, value in group.items():
            group[key] = len(value)
        return group

    return transformer
