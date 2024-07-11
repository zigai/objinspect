import typing as T
from enum import EnumMeta
from types import FunctionType

import typing_extensions

from objinspect.constants import EMPTY


def type_to_str(t: T.Any) -> str:
    """
    Convert a Python type to its string representation (without the module name).

    Args:
        t (Any): A type.

    Returns:
        str: The string representation of the Python type.

    Example:
    ```python
    >>> type_to_str(datetime.datetime)
    'datetime'
    >>> type_to_str(int)
    'int'
    ```
    """
    type_str = repr(t)
    if "<class '" in type_str:
        type_str = type_str.split("'")[1]
    return type_str.split(".")[-1]


def call_method(obj: object, name: str, args: tuple = (), kwargs: dict = {}) -> T.Any:
    """
    Call a method with the given name on the given object.

    Args:
        obj (object): The object to call the method on.
        name (str): The name of the method to call.
        args (tuple, optional): The positional arguments to pass to the method.
        kwargs (dict, optional): The keyword arguments to pass to the method.

    Returns:
        object: The result of calling the method.

    Example:
    ```python
    >>> import math
    >>> call_method(math, "pow", args=(2, 2))
    4.0
    ```
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


def is_enum(t: T.Any) -> bool:
    return isinstance(t, EnumMeta)


def get_enum_choices(e) -> tuple[str, ...]:
    """
    Get the options of a Python Enum.

    Args:
        e (enum.Enum): A Python Enum.

    Returns:
        tuple: A tuple of the names of the Enum options.

    Example:
    ```python
    >>> import enum
    >>> class Color(enum.Enum):
    ...     RED = 1
    ...     GREEN = 2
    ...     BLUE = 3
    >>> get_enum_choices(Color)
    ('RED', 'GREEN', 'BLUE')
    ```
    """
    return tuple(e.__members__.keys())


def is_direct_literal(t: T.Any) -> bool:
    """
    Determine if the given type is a 'pure' Literal type.
    It checks if the input type is a direct instance of Literal,
    not including the Literal class itself. This function distinguishes between the
    Literal class itself and instantiated Literal types. It returns True only for the latter.

    Args:
        t (Any): The type to check.

    Returns:
        bool: True if the type is a pure Literal, False otherwise.

    Example:
    ```python
    >>> from typing_extensions import Literal
    >>> is_direct_literal(Literal[1, 2, 3])
    True
    >>> is_direct_literal(Literal)
    False
    >>> is_direct_literal(int)
    False
    >>> is_direct_literal(Union[str, Literal[1, 2]])
    False
    ```
    """
    if t is typing_extensions.Literal:
        return False
    if hasattr(t, "__origin__") and t.__origin__ is typing_extensions.Literal:
        return True
    return False


def is_or_contains_literal(t: T.Any) -> bool:
    """
    Determine if the given type is a Literal type or contains a Literal type.

    Example:
    ```python
    >>> from typing import Union, Optional
    >>> from typing_extensions import Literal
    >>> is_or_contains_literal(Literal[1, 2, 3])
    True
    >>> is_or_contains_literal(Union[int, Literal[1, 2]])
    True
    >>> is_or_contains_literal(Optional[Literal['a', 'b']])
    True
    >>> is_or_contains_literal(int)
    False
    ```
    """
    if is_direct_literal(t):
        return True

    for i in T.get_args(t):
        if is_or_contains_literal(i):
            return True
    return False


def get_literal_choices(literal_t) -> tuple[str, ...]:
    """
    Get the options of a Python Literal.
    """
    if is_direct_literal(literal_t):
        return T.get_args(literal_t)
    for i in T.get_args(literal_t):
        if is_direct_literal(i):
            return T.get_args(i)
    raise ValueError(f"{literal_t} is not a literal")


def literal_contains(literal_type, value: T.Any) -> bool:
    """
    Check if a value is in a Python Literal.
    """
    if not is_direct_literal(literal_type):
        raise ValueError(f"{literal_type} is not a literal")

    values = get_literal_choices(literal_type)
    if not len(values):
        raise ValueError(f"{literal_type} has no values")
    return value in values


def create_function(
    name: str,
    args: dict[str, T.Tuple[T.Any, T.Any]],
    body: str | list[str],
    globs: dict[str, T.Any],
    return_type: T.Any | EMPTY = EMPTY,
    docstring: str | None = None,
) -> T.Callable[..., T.Any]:
    """
    Create a function with the given name, arguments, body, and globals.

    Args:
        name (str): The name of the function.
        args (dict): A dictionary mapping argument names to tuples of the argument type and default value.
        body (str | list): The body of the function. If it's a string, it will be split by newlines.
        globs (dict): The globals to use when executing the function.
        return_type (Any, optional): The return type of the function.
        docstring (str, optional): The docstring of the function.

    Example:
    ```python
    >>> add = create_function(
    ...     name="add",
    ...     args={
    ...         "a": (int, None),
    ...         "b": (int, 2),
    ...     },
    ...     body=[
    ...         "result = a + b",
    ...         "return result",
    ...          ],
    ...     docstring="Adds two numbers together. If b is not provided it defaults to 2.",
    ...     globs=globals(),
    ...   )
    >>> add(2, 2)
    4
    ```
    """

    arg_str = []
    for arg, annotations in args.items():
        if len(annotations) == 2:
            t, default = annotations
        elif len(annotations) == 1:
            t = annotations[0]
            default = EMPTY
        else:
            raise ValueError(f"Invalid annotations for argument {arg}: {annotations}")

        if t is not EMPTY:
            arg_str.append(f"{arg}: {t.__name__}")
        else:
            arg_str.append(arg)
        if default is not EMPTY:
            arg_str[-1] += f" = {repr(default)}"

    arg_str = ", ".join(arg_str)
    body_str = "\n    ".join(body) if isinstance(body, list) else body
    func_str = f"def {name}({arg_str})"

    if return_type is not EMPTY:
        if return_type is None:
            func_str += " -> None"
        else:
            func_str += f" -> {return_type.__name__}"

    func_str += ":"
    if docstring:
        func_str += f'\n    """{docstring}"""'
    func_str += f"\n    {body_str}"

    code_obj = compile(func_str, "<string>", "exec")
    exec(code_obj, globs)
    func = globs[name]
    func.__annotations__ = {arg: annotation[0] for arg, annotation in args.items()}
    if return_type is not EMPTY:
        func.__annotations__["return"] = return_type

    return func


__all__ = [
    "type_to_str",
    "get_enum_choices",
    "get_literal_choices",
    "call_method",
    "get_uninherited_methods",
    "is_enum",
    "is_or_contains_literal",
]
