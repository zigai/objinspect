import inspect

from objinspect import constants, util
from objinspect._class import Class
from objinspect.function import Function
from objinspect.parameter import Parameter


def objinspect(object, include_inherited: bool = True):
    """
    The objinspect function takes an `object` and an optional `include_inherited` flag (defaults to True) and returns either a `Function` or a `Class` object  representing its structure.

    Args:
        object (object): The object to be inspected.
        include_inherited (bool, optional): Whether to include inherited attributes and methods in the inspection. Defaults to True.

    Returns:
        Either a Function object or a Class object depending on the type of object.
    Example:
        >>> objinspect(objinspect)
        >>> Function(name='objinspect', parameters=2, description='The objinspect function takes an object and an optional include_inherited flag (defaults to True) and returns either a Function object or a Class object depending on the type of object.')
        >>>
        >>> import math
        >>> objinspect(math.pow)
        Function(name='pow', parameters=2, description='Return x**y (x to the power of y).')
        >>>
        >>> objinspect(math.pow).dict
        {'name': 'pow', 'parameters': [{'name': 'x', 'kind': <_ParameterKind.POSITIONAL_ONLY: 0>, 'type': <class 'inspect._empty'>, 'default': <class 'inspect._empty'>, 'description': None}, {'name': 'y', 'kind': <_ParameterKind.POSITIONAL_ONLY: 0>, 'type': <class 'inspect._empty'>, 'default': <class 'inspect._empty'>, 'description': None}], 'docstring': 'Return x**y (x to the power of y).'}
    """
    if inspect.isclass(object):
        return Class(object, include_inherited)
    return Function(object)
