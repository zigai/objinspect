import inspect

from interfacy_core import util
from interfacy_core.constants import EMPTY, SPECIAL_GENERIC_ALIAS, UNION_GENERIC_ALIAS
from interfacy_core.exceptions import InterfacyException, UnsupportedParamError
from interfacy_core.interfacy_class import InterfacyClass
from interfacy_core.interfacy_func import InterfacyFunction, InterfacyParameter


def process_obj(obj, *args):
    if inspect.isfunction(obj):
        return InterfacyFunction(obj)
    if inspect.isclass(obj):
        cls = InterfacyClass(obj)
        for i in cls.methods.keys():
            if i == "__init__":
                continue
            if i not in args:
                del cls.methods[i]
        return cls
    raise TypeError(obj)
