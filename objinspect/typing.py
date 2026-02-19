import types
import typing
from collections import defaultdict, deque
from collections.abc import Iterable, Mapping
from enum import EnumMeta

import typing_extensions

UNION_ORIGINS = {typing.Union, types.UnionType}


def _flatten_union_args(t: object) -> list[object]:
    """Flatten nested union arguments into a linear list."""
    flattened: list[object] = []
    for arg in typing.get_args(t):
        if is_union_type(arg):
            flattened.extend(_flatten_union_args(arg))
        else:
            flattened.append(arg)
    return flattened


def type_name(t: object) -> str:
    """
    Convert a Python type to its string representation (without the module name).

    Args:
        t (object): A Python type.

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
    name = name.rsplit(".", maxsplit=1)[-1]
    if "| None" in name:
        name = name.replace("| None", "").strip()
        name += "?"
    return name


def is_generic_alias(t: object) -> bool:
    """
    Check if a type is an alias type (list[str], dict[str, int], etc...]).

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
    return isinstance(t, types.GenericAlias) or (
        type(t).__module__ == "typing" and type(t).__name__ == "_GenericAlias"
    )


def is_union_type(t: object) -> bool:
    """
    Check if a type is a union type (float | int, str | None, etc...).

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
    return typing.get_origin(t) in UNION_ORIGINS


def is_iterable_type(t: object) -> bool:
    """
    Check if a type is an iterable type (list, tuple, etc...).

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
    origin = typing.get_origin(t)
    if origin is not None:
        t = origin
    if t in typing_iterables:
        return True

    try:
        return issubclass(t, Iterable)
    except TypeError:
        return False


def is_mapping_type(t: object) -> bool:
    """
    Check if a type is a mapping type (dict, OrderedDict, etc...).

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
    origin = typing.get_origin(t)
    if origin is not None:
        t = origin
    if t in typing_mappings:
        return True

    try:
        return issubclass(t, Mapping)
    except TypeError:
        return False


def type_simplified(t: object) -> object | tuple[object, ...]:
    """
    Simplify parametrized types to their origins.

    Example:
        ```python
        >>> type_simplify(list[str])
        <class 'list'>
        >>> type_simplify(float | list[str])
        (<class 'float'>, <class 'list'>)
        ```
    """
    origin = type_origin(t)
    if origin is None:
        return t

    if is_union_type(t):
        args = type_args(t)
        return tuple(type_simplified(i) for i in args)

    return origin


def is_enum(t: object) -> bool:
    """Check if a type is an Enum type."""
    return isinstance(t, EnumMeta)


def get_enum_choices(e: object) -> tuple[str, ...]:
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


def is_direct_literal(t: object) -> bool:
    """
    Determine if the given type is a 'pure' Literal type.
    It checks if the input type is a direct instance of Literal,not including the Literal class itself.
    This function distinguishes between the 'Literal' class itself and instantiated Literal types. It returns True only for the latter.

    Args:
        t (object): The type to check.

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
    return hasattr(t, "__origin__") and t.__origin__ is typing_extensions.Literal


def is_or_contains_literal(t: object) -> bool:
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

    return any(is_or_contains_literal(i) for i in typing.get_args(t))


def get_literal_choices(literal_t: object) -> tuple[object, ...]:
    """Get the options of a Python Literal."""
    if is_direct_literal(literal_t):
        return typing.get_args(literal_t)
    for i in typing.get_args(literal_t):
        if is_direct_literal(i):
            return typing.get_args(i)
    raise ValueError(f"{literal_t} is not a literal")


def literal_contains(literal_t: object, value: object) -> bool:
    """Check if a value is in a Python Literal."""
    if not is_direct_literal(literal_t):
        raise ValueError(f"{literal_t} is not a literal")

    values = get_literal_choices(literal_t)
    if not len(values):
        raise ValueError(f"{literal_t} has no values")
    return value in values


def get_choices(t: object) -> tuple[object, ...] | None:
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
        choices: list[object] = []
        for i in args:
            if is_enum(i):
                choices.extend(get_enum_choices(i))
            elif is_or_contains_literal(i):
                choices.extend(get_literal_choices(i))
        return tuple(choices)
    return None


def type_origin(t: object) -> object | None:
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


def type_args(t: object) -> tuple[object, ...]:
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
    "get_enum_choices",
    "get_literal_choices",
    "is_direct_literal",
    "is_enum",
    "is_generic_alias",
    "is_iterable_type",
    "is_mapping_type",
    "is_or_contains_literal",
    "is_union_type",
    "literal_contains",
    "type_args",
    "type_name",
    "type_origin",
    "type_simplified",
]
