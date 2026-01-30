import inspect as _inspect
from collections.abc import Callable
from typing import Any

from objinspect._class import Class
from objinspect.function import Function
from objinspect.method import Method, MethodFilter
from objinspect.parameter import Parameter


def inspect(
    obj: object,
    init: bool = True,
    public: bool = True,
    inherited: bool = True,
    static_methods: bool = True,
    classmethod: bool = False,
    protected: bool = False,
    private: bool = False,
) -> Function | Class | Method:
    """
    Inspects an object and returns a structured representation of its attributes and methods.

    This function analyzes the given object and returns either a `Function`, `Class`, or `Method` which
    encapsulates the object's structure, including its name, parameters, docstring, and other relevant information.
    The inspection can be customized to include or exclude certain types of attributes and methods
    based on the provided boolean flags.

    Args:
        obj (object): The object to be inspected.
        init (bool, optional): Whether to include the __init__ method for classes.
        public (bool, optional): Whether to include public attributes and methods.
        inherited (bool, optional): Whether to include inherited attributes and methods.
        static_methods (bool, optional): Whether to include static methods.
        classmethod (bool, optional): Whether to include class methods.
        protected (bool, optional): Whether to include protected attributes and methods (prefixed with _).
        private (bool, optional): Whether to include private attributes and methods (prefixed with __).

    Returns:
        An object representing the structure of the inspected object.

    Example:
    ```python
        >>> from objinspect import inspect, pdir
        >>> import math
        >>> inspect(math.pow)
        Function(name='pow', parameters=2, description='Return x**y (x to the power of y).')

        >>> inspect(math.pow).dict
        {
        'name': 'pow',
        'parameters': [
            {'name': 'x', 'kind': <_ParameterKind.POSITIONAL_ONLY: 0>, 'type': <class 'inspect._empty'>, 'default': <class 'inspect._empty'>, 'description': None},
            {'name': 'y', 'kind': <_ParameterKind.POSITIONAL_ONLY: 0>, 'type': <class 'inspect._empty'>, 'default': <class 'inspect._empty'>, 'description': None}],
        'docstring': 'Return x**y (x to the power of y).'
        }

        >>> inspect(inspect)
        Function(name='inspect', parameters=8, description='Inspects an object and returns a structured representation of its attributes and methods.')
    ```
    """
    if _inspect.ismethod(obj):
        return Method(obj, obj.__self__.__class__)

    if _inspect.isfunction(obj):
        cls = get_class_from_method(obj)
        if cls is None:
            return Function(obj)
        return Method(obj, cls)

    return Class(
        obj,
        init=init,
        public=public,
        inherited=inherited,
        static_methods=static_methods,
        classmethod=classmethod,
        protected=protected,
        private=private,
    )


def get_class_from_method(method: Callable[..., Any]) -> type | None:
    """
    Get the class that defines a given method.

    Args:
        method (Callable): The method to analyze.

    Returns:
        type | None: The class that defines the method, or None if not found.
    """
    qualname = method.__qualname__
    module = _inspect.getmodule(method)
    if "." in qualname:
        parts = qualname.split(".")
        if module:
            cls = module
            for part in parts[:-1]:
                if hasattr(cls, part):
                    cls = getattr(cls, part)
                else:
                    return None
            if isinstance(cls, type) and method.__name__ in cls.__dict__:
                return cls
    return None


__all__ = [
    "inspect",
    "Class",
    "Function",
    "Method",
    "Parameter",
    "MethodFilter",
]
