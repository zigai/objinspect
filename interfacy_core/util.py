import os
import types
import typing

from docstring_parser import Docstring

from interfacy_core.constants import UNION_TYPE


def has_docstring(docstring: str | None) -> bool:
    if docstring is None:
        return False
    return len(docstring) != 0


def docstring_description(docstring: Docstring | None) -> str:
    if docstring is None:
        return ""
    if docstring.short_description:
        return docstring.short_description
    if docstring.long_description:
        return docstring.long_description
    return ""


class UnionParameter:
    def __init__(self, params: tuple) -> None:
        self.params = params

    def __iter__(self):
        for i in self.params:
            yield i

    def __repr__(self) -> str:
        params = [type_as_str(i) for i in self.params]
        params = " | ".join(params)
        return f"{self.__class__.__name__}({params})"


def type_as_str(t):
    type_str = repr(t)
    if "<class '" in type_str:
        type_str = type_str.split("'")[1]
    return type_str.split(".")[-1]


def get_enum_opts(e):
    return tuple(e.__members__.keys())


def is_file(path):
    return os.path.isfile(path)


def simplify_type(t, depth: int = -1):
    if depth == 0:
        return t
    if depth > 0:
        depth -= 1
    origin = typing.get_origin(t)
    if type(origin) is types.NoneType:
        return t

    if origin in UNION_TYPE:
        origin = typing.get_args(t)
        return UnionParameter(tuple(simplify_type(i, depth=depth) for i in origin))
    return simplify_type(origin, depth=depth)


def call_bound_method(obj: object, name: str, obj_args: dict = {}, method_args: dict = {}):
    return obj(**obj_args).__getattribute__(name)(**method_args)


def split_type_hint(t):
    """
    (Base, Sub)
    list[int] -> (list,int)
    """
    return typing.get_origin(t), typing.get_args(t)
