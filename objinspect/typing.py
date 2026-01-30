import types
import typing
from collections import defaultdict, deque
from collections.abc import Iterable, Mapping
from enum import EnumMeta
from typing import Any

import typing_extensions

ALIAS_TYPES = [typing._GenericAlias, types.GenericAlias]  # type:ignore
UNION_TYPES = [typing._UnionGenericAlias, types.UnionType]  # type:ignore


def _flatten_union_args(t: Any) -> list[Any]:
    """Flatten nested union arguments into a linear list."""
    flattened: list[Any] = []
    for arg in typing.get_args(t):
        if is_union_type(arg):
            flattened.extend(_flatten_union_args(arg))
        else:
            flattened.append(arg)
    return flattened


def type_name(t: Any) -> str:
    """
    Convert a Python type to its string representation (without the module name).

    Args:
        t (Any): A Python type.

    Returns:
        str: The string representation of the Python type.

    Example:
        ```python
        >>> type_to_str(datetime.datetime)
        'datetime'
        >>> type_to_str(int)
        'int'
        ```
    """
    if is_union_type(t):
        union_args = _flatten_union_args(t) or (t,)
        return " | ".join(type_name(arg) for arg in union_args)

    type_str = repr(t)
    if "<class '" in type_str:
        type_str = type_str.split("'")[1]
    return type_str.split(".")[-1]


def simplified_type_name(name: str) -> str:
    """Simplifies the type name by removing module paths and optional "None" union."""
    name = name.split(".")[-1]
    if "| None" in name:
        name = name.replace("| None", "").strip()
        name += "?"
    return name


def is_generic_alias(t: Any) -> bool:
    """
    Check if a type is an alias type (list[str], dict[str, int], etc...])

    Example:
        ```python
        >>> is_generic_alias(list[str])
        True
        >>> is_generic_alias(int)
        False
        >>> String = str
        >>> is_generic_alias(String)
        False
        ```
    """
    return type(t) in ALIAS_TYPES


def is_union_type(t: Any) -> bool:
    """
    Check if a type is a union type (float | int, str | None, etc...)

    Example:
        ```python
        >>> is_union_type(int | str)
        True
        >>> from typing import Union
        >>> is_union_type(Union[int, str])
        True
        >>> is_union_type(list)
        False
        ```
    """
    return type(t) in UNION_TYPES


def is_iterable_type(t: Any) -> bool:
    """
    Check if a type is an iterable type (list, tuple, etc...)

    Example:
        ```python
        >>> is_iterable_type(list)
        True
        >>> is_iterable_type(dict)
        True
        >>> is_iterable_type(int)
        False
        >>> is_iterable_type(typing.List)
        True
        >>> is_iterable_type(typing.Dict)
        True
        ```
    """
    typing_iterables = [
        list,
        tuple,
        dict,
        set,
        frozenset,
        deque,
        defaultdict,
        typing.List,  # noqa: UP006
        typing.Dict,  # noqa: UP006
        typing.Set,  # noqa: UP006
        typing.Deque,  # noqa: UP006
        typing.Sequence,
        typing.OrderedDict,
        typing.ChainMap,
        typing.Counter,
        typing.Generator,
        typing.AsyncGenerator,
        typing.Iterable,
        typing.Collection,
        typing.AbstractSet,
        typing.MutableSet,
        typing.Mapping,
        typing.MutableMapping,
        typing.MutableSequence,
    ]
    if isinstance(t, (types.GenericAlias, typing._GenericAlias)):  # type:ignore
        t = t.__origin__
    if t in typing_iterables:
        return True

    try:
        return issubclass(t, Iterable)
    except TypeError:
        return False


def is_mapping_type(t: Any) -> bool:
    """
    Check if a type is a mapping type (dict, OrderedDict, etc...)

    Example:
        ```python
        >>> is_mapping_type(dict)
        True
        >>> is_mapping_type(list)
        False
        >>> is_mapping_type(typing.Dict)
        True
        >>> is_mapping_type(typing.OrderedDict)
        True
        ```
    """
    typing_mappings = [
        dict,
        typing.Dict,  # noqa: UP006
        typing.Mapping,
        typing.MutableMapping,
        defaultdict,
        typing.DefaultDict,  # noqa: UP006
        typing.OrderedDict,
        typing.ChainMap,
    ]
    if isinstance(t, (types.GenericAlias, typing._GenericAlias)):  # type:ignore
        t = t.__origin__
    if t in typing_mappings:
        return True

    try:
        return issubclass(t, Mapping)
    except TypeError:
        return False


def type_simplified(t: Any) -> Any | tuple[Any, ...]:
    """
    Example:
        ```python
        >>> type_simplify(list[str])
        <class 'list'>
        >>> type_simplify(float | list[str])
        (<class 'float'>, <class 'list'>)
        ```
    """
    origin = type_origin(t)
    if isinstance(type(origin), types.NoneType) or origin is None:
        return t

    if is_union_type(t):
        args = type_args(t)
        return tuple([type_simplified(i) for i in args])

    return origin


def is_enum(t: Any) -> bool:
    """Check if a type is an Enum type."""
    return isinstance(t, EnumMeta)


def get_enum_choices(e: Any) -> tuple[str, ...]:
    """
    Get the options of a Python Enum.

    Args:
        e (enum.Enum): A Python Enum.

    Returns:
        tuple: A tuple of the names of the Enum options.

    Example:
        ```python
        >>> import enum
        >>> class Color(enum.Enum):
        ...     RED = 1
        ...     GREEN = 2
        ...     BLUE = 3
        >>> get_enum_choices(Color)
        ('RED', 'GREEN', 'BLUE')
        ```
    """
    if not is_enum(e):
        raise TypeError(f"'{e}' is not an Enum")
    return tuple(e.__members__.keys())


def is_direct_literal(t: Any) -> bool:
    """
    Determine if the given type is a 'pure' Literal type.
    It checks if the input type is a direct instance of Literal,not including the Literal class itself.
    This function distinguishes between the 'Literal' class itself and instantiated Literal types. It returns True only for the latter.

    Args:
        t (Any): The type to check.

    Returns:
        bool: True if the type is a pure Literal, False otherwise.

    Example:
        ```python
        >>> from typing_extensions import Literal
        >>> is_direct_literal(Literal[1, 2, 3])
        True
        >>> is_direct_literal(Literal)
        False
        >>> is_direct_literal(int)
        False
        >>> is_direct_literal(Union[str, Literal[1, 2]])
        False
        ```
    """
    if t is typing_extensions.Literal:
        return False
    if hasattr(t, "__origin__") and t.__origin__ is typing_extensions.Literal:
        return True
    return False


def is_or_contains_literal(t: Any) -> bool:
    """
    Determine if the given type is a Literal type or contains a Literal type.

    Example:
        ```python
        >>> from typing import Union, Optional
        >>> from typing_extensions import Literal
        >>> is_or_contains_literal(Literal[1, 2, 3])
        True
        >>> is_or_contains_literal(Union[int, Literal[1, 2]])
        True
        >>> is_or_contains_literal(Optional[Literal['a', 'b']])
        True
        >>> is_or_contains_literal(int)
        False
        ```
    """
    if is_direct_literal(t):
        return True

    for i in typing.get_args(t):
        if is_or_contains_literal(i):
            return True
    return False


def get_literal_choices(literal_t: Any) -> tuple[str, ...]:
    """Get the options of a Python Literal."""
    if is_direct_literal(literal_t):
        return typing.get_args(literal_t)
    for i in typing.get_args(literal_t):
        if is_direct_literal(i):
            return typing.get_args(i)
    raise ValueError(f"{literal_t} is not a literal")


def literal_contains(literal_t: Any, value: Any) -> bool:
    """Check if a value is in a Python Literal."""
    if not is_direct_literal(literal_t):
        raise ValueError(f"{literal_t} is not a literal")

    values = get_literal_choices(literal_t)
    if not len(values):
        raise ValueError(f"{literal_t} has no values")
    return value in values


def get_choices(t: Any) -> tuple[Any, ...] | None:
    """
    Try to get the choices of a Literal or Enum type.
    Will also work with a Union type that contains Literal or Enum types.
    Returns None if the type is not a Literal or Enum.
    """
    if is_or_contains_literal(t):
        return get_literal_choices(t)
    if is_enum(t):
        return get_enum_choices(t)
    if is_union_type(t):
        args = type_args(t)
        choices: list[Any] = []
        for i in args:
            if is_enum(i):
                choices.extend(get_enum_choices(i))
            elif is_or_contains_literal(i):
                choices.extend(get_literal_choices(i))
        return tuple(choices)
    return None


def type_origin(t: Any) -> Any:
    """
    A wrapper for typing.get_origin to get the origin of a type.

    Example:
        ```python
        >>> type_args(list[list[str]])
        <class 'list'>
        >>> type_origin(float | int)
        <class 'types.UnionType'>
        ```
    """
    return typing.get_origin(t)


def type_args(t: Any) -> tuple[Any, ...]:
    """
    A wrapper for typing.get_args to get the arguments of a type.

    Example:
        ```python
        >>> type_args(list[str])
        (<class 'str'>,)
        >>> type_args(dict[str, int])
        (<class 'str'>, <class 'int'>)
        >>> type_args(list[list[str]])
        (list[str],)
        ```
    """
    return typing.get_args(t)


__all__ = [
    "type_name",
    "is_generic_alias",
    "is_union_type",
    "is_iterable_type",
    "is_mapping_type",
    "type_simplified",
    "is_enum",
    "get_enum_choices",
    "is_direct_literal",
    "is_or_contains_literal",
    "get_literal_choices",
    "literal_contains",
    "type_origin",
    "type_args",
]
