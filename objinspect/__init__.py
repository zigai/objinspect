import inspect

from objinspect import constants, util
from objinspect._class import Class
from objinspect.function import Function
from objinspect.method import Method, MethodFilter
from objinspect.parameter import Parameter


def objinspect(
    obj,
    init=True,
    public=True,
    inherited=True,
    static_methods=True,
    protected=False,
    private=False,
):
    """
    The objinspect function takes an `object` and an optional `include_inherited` flag (defaults to True) and returns either a `Function` or a `Class` object  representing its structure.

    Args:
        obj (object): The object to be inspected.
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
    if inspect.isclass(obj):
        return Class(
            obj,
            init=init,
            public=public,
            inherited=inherited,
            static_methods=static_methods,
            protected=protected,
            private=private,
        )
    return Function(obj)
