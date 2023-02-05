import inspect
import types
import typing

inspect._empty.__repr__ = lambda: "EMPTY"
inspect._empty.__str__ = lambda: "EMPTY"
EMPTY = inspect._empty
SPECIAL_GENERIC_ALIAS = typing._SpecialGenericAlias  # type: ignore
UNION_GENERIC_ALIAS = typing._UnionGenericAlias  # type: ignore
ALIAS_TYPE = [SPECIAL_GENERIC_ALIAS, types.GenericAlias]
UNION_TYPE = [UNION_GENERIC_ALIAS, types.UnionType]

__all__ = [
    "EMPTY",
    "SPECIAL_GENERIC_ALIAS",
    "UNION_GENERIC_ALIAS",
    "ALIAS_TYPE",
    "UNION_TYPE",
]
