from inspect import _ParameterKind
from types import FunctionType
from typing import Any

from objinspect._class import Class
from objinspect.function import Function
from objinspect.method import Method


def type_to_str(t: Any) -> str:
    """
    Convert a Python type to its string representation (without the module name).

    Args:
        t (Any): A Python type.

    Returns:
        str: The string representation of the Python type.

    Example:
        >>> type_to_str(datetime.datetime)
        'datetime'
        >>> type_to_str(int)
        'int'
    """
    type_str = repr(t)
    if "<class '" in type_str:
        type_str = type_str.split("'")[1]
    return type_str.split(".")[-1]


def get_enum_choices(e) -> tuple[str, ...]:
    """
    Get the options of a Python Enum.

    Args:
        e (enum.Enum): A Python Enum.

    Returns:
        tuple: A tuple of the names of the Enum options.

    Example:
        >>> import enum
        >>> class Color(enum.Enum):
        ...     RED = 1
        ...     GREEN = 2
        ...     BLUE = 3
        >>> get_enum_choices(Color)
        ('RED', 'GREEN', 'BLUE')
    """
    return tuple(e.__members__.keys())


def call_method(obj: object, name: str, args: tuple = (), kwargs: dict = {}) -> Any:
    """
    Call a method with the given name on the given object.

    Args:
        obj (object): The object to call the method on.
        name (str): The name of the method to call.
        args (tuple, optional): The positional arguments to pass to the method. Defaults to ().
        kwargs (dict, optional): The keyword arguments to pass to the method. Defaults to {}.

    Returns:
        object: The result of calling the method.

    Examples:
    >>> import math
    >>> call_method(math, "pow", args=(2, 2))
    4.0
    """
    return getattr(obj, name)(*args, **kwargs)


def get_uninherited_methods(cls) -> list[str]:
    """
    Get the methods of a class that are not inherited from its parent classes.
    """
    return [
        name
        for name, method in cls.__dict__.items()
        if isinstance(method, (FunctionType, classmethod, staticmethod))
    ]


def split_args_kwargs(func_args: dict, func: Function | Method) -> tuple[tuple, dict]:
    """
    Split the arguments passed to a function into positional and keyword arguments.
    """
    args, kwargs = [], {}
    for param in func.params:
        if param.kind == _ParameterKind.POSITIONAL_ONLY:
            args.append(func_args[param.name])
        else:
            kwargs[param.name] = func_args[param.name]
    return tuple(args), kwargs


def split_init_args(args: dict, cls: Class, method: Method) -> tuple[dict, dict]:
    """
    Split the arguments into those that should be passed to the __init__ method and those that should be passed to the method.
    """
    if not method.is_static and cls.has_init:
        init_method = cls.get_method("__init__")
        init_arg_names = [i.name for i in init_method.params]
        args_init = {k: v for k, v in args.items() if k in init_arg_names}
        args_method = {k: v for k, v in args.items() if k not in init_arg_names}
        return args_init, args_method
    return {}, args


__all__ = [
    "type_to_str",
    "get_enum_choices",
    "call_method",
    "get_uninherited_methods",
    "split_args_kwargs",
    "split_init_args",
]
