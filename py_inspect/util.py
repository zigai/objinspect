import types
import typing
from types import FunctionType
from typing import Any

from py_inspect.constants import UNION_TYPE


def type_to_str(t) -> str:
    type_str = repr(t)
    if "<class '" in type_str:
        type_str = type_str.split("'")[1]
    return type_str.split(".")[-1]


def get_enum_options(e):
    return tuple(e.__members__.keys())


def call_method(obj: object, name: str, args: tuple = (), kwargs: dict = {}):
    """
    Examples:
    >>> import math
    >>> call_method(math, "pow", args=(2, 2))
    4.0
    """
    return obj.__getattribute__(name)(*args, **kwargs)


def type_origin(t: Any):
    """
    typing.get_origin wrapper
    Examples:
    >>> type_args(list[list[str]])
    <class 'list'>
    >>> type_origin(float | int)
    <class 'types.UnionType'>
    """
    return typing.get_origin(t)


def type_args(t: Any):
    """
    typing.get_args wrapper

    Examples:
    >>> type_args(list[str])
    (<class 'str'>,)
    >>> type_args(dict[str, int])
    (<class 'str'>, <class 'int'>)
    >>> type_args(list[list[str]])
    (list[str],)
    """
    return typing.get_args(t)


class UnionParameter:
    def __init__(self, params: tuple) -> None:
        self.params = params

    def __iter__(self):
        for i in self.params:
            yield i

    def __repr__(self) -> str:
        params = [type_to_str(i) for i in self.params]
        params = " | ".join(params)
        return f"{self.__class__.__name__}({params})"

    @classmethod
    def from_type(cls, t):
        if type(t) in UNION_TYPE:
            return cls(type_args(t))
        raise TypeError(t)


def type_simplify(t: Any):
    """
    Examples:
    >>> type_simplify(list[str])
    <class 'list'>
    >>> type_simplify(float | list[str])
    UnionParameter(float | list)
    """
    origin = type_origin(t)
    if type(origin) is types.NoneType:
        return t
    if origin in UNION_TYPE:
        origin = type_args(t)
        return UnionParameter(tuple(type_simplify(i) for i in origin))
    return origin


def get_methods(cls) -> list[str]:
    """
    Get names of methods that belong to a class. Do not incdule inherited methods.
    """
    return list(
        name
        for name, method in cls.__dict__.items()
        if isinstance(method, (FunctionType, classmethod, staticmethod))
    )


__all__ = [
    "UnionParameter",
    "type_to_str",
    "get_enum_options",
    "call_method",
    "type_origin",
    "type_args",
    "type_simplify",
    "get_methods",
]
