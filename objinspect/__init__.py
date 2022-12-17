import inspect

from objinspect import constants, util
from objinspect._class import Class
from objinspect.function import Function
from objinspect.parameter import Parameter


def objinspect(object, include_inherited: bool = True):
    if inspect.isfunction(object) or inspect.ismethod(object):
        return Function(object)
    return Class(object, include_inherited)
