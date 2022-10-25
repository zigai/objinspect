import inspect as _inspect

from py_inspect import constants, util
from py_inspect._class import Class
from py_inspect.function import Function
from py_inspect.parameter import Parameter


def inspect(object):
    if _inspect.isfunction(object) or _inspect.ismethod(object):
        return Function(object)
    return Class(object)
