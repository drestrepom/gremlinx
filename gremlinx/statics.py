# Standar library
from typing import (
    Any,
    Callable,
    Tuple,
    Union,
)

# Third libraries
from mypy_extensions import (
    VarArg,
    NamedArg,
)

# Local imports
from gremlinx.utils.statics import (
    has as _has,
    hasLabel as _hasLabel,
)


def has(
    *args: str
) -> Tuple[Callable[[
        VarArg(Any),
        NamedArg(Any, 'traversal'),
        NamedArg(Union[str, Tuple[str, str]], 'vertex')
], bool], Tuple[str, ...], None]:
    return _has, args, None


def hasLabel(
    *labels: str
) -> Tuple[Callable[[
        VarArg(Any),
        NamedArg(Any, 'traversal'),
        NamedArg(Union[str, Tuple[str, str]], 'vertex')
], bool], Tuple[str, ...], None]:
    return _hasLabel, labels, None
