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
