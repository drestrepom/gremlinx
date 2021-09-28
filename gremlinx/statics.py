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
    for n_id in group.keys():
        label_name = group.graph_traversal.graph.nodes[n_id].get("labelV")
        if label_name in new_dict:
            new_dict[label_name].append(n_id)
        else:
            new_dict[label_name] = [n_id]

    return new_dict
