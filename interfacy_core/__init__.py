import inspect

from interfacy_core.constants import (
    ALIAS_TYPE,
    EMPTY,
    SPECIAL_GENERIC_ALIAS,
    UNION_GENERIC_ALIAS,
    UNION_TYPE,
)
from interfacy_core.exceptions import InterfacyException, UnsupportedParamError
from interfacy_core.interfacy_class import InterfacyClass
from interfacy_core.interfacy_func import InterfacyFunction, InterfacyParameter
from interfacy_core.util import *


def process_obj(obj, *args):
    if inspect.isfunction(obj):
        return InterfacyFunction(obj)
    if inspect.isclass(obj):
        cls = InterfacyClass(obj)
        cpy = cls.methods.copy()
        for i in cls.methods.keys():
            if i == "__init__":
                continue
            if i.startswith("__"):
                del cpy[i]
        if args:
            for i in cls.methods.keys():
                if i == "__init__":
                    continue
                if i not in args:
                    del cpy[i]
        cls.methods = cpy
        return cls
    raise TypeError(obj)
