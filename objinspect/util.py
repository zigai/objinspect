from collections.abc import Callable
from types import FunctionType
from typing import Any

from stdl.st import TextStyle, with_style

from objinspect.constants import EMPTY
from objinspect.typing import simplified_type_name, type_name


def call_method(
    obj: object,
    name: str,
    args: tuple[Any, ...] = (),
    kwargs: dict[str, Any] | None = None,
) -> Any:
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
    kwargs = kwargs or {}
    return getattr(obj, name)(*args, **kwargs)


def get_uninherited_methods(cls: type) -> list[str]:
    """Get the methods of a class that are not inherited from its parent classes."""
    return [
        name
        for name, method in cls.__dict__.items()
        if isinstance(method, (FunctionType, classmethod, staticmethod))
    ]


def create_function(
    name: str,
    args: dict[str, tuple[Any, Any]],
    body: str | list[str],
    globs: dict[str, Any],
    return_type: Any | EMPTY = EMPTY,
    docstring: str | None = None,
) -> Callable[..., Any]:
    """
    Create a function with the given name, arguments, body, and globals.

    Args:
        name (str): The name of the function.
        args (dict): A dictionary mapping argument names to tuples of the argument type and default value.
        body (str | list): The body of the function. If a string, it will be split by newlines.
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
        ...     docstring="Adds two numbers together. If b is not provided, defaults to 2.",
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

    arg_str_final = ", ".join(arg_str)
    body_str = "\n    ".join(body) if isinstance(body, list) else body
    func_str = f"def {name}({arg_str_final})"

    if return_type is not EMPTY:
        if return_type is None:
            func_str += " -> None"
        elif hasattr(return_type, "__name__"):
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


def colored_type(
    t: type,
    style: TextStyle,
    simplify: bool = True,
) -> str:
    """
    Return a colored string representation of a type.

    Args:
        t (type): The type to format.
        style (TextStyle): The text style (color) to apply.
        simplify (bool, optional): Whether to simplify the type name. Defaults to True.
    """
    text = type_name(t)
    if simplify:
        text = simplified_type_name(text)
    NO_COLOR_CHARS = "[](){}|,?"
    colored_segments: list[str] = []
    current_segment: list[str] = []
    for char in text:
        if char in NO_COLOR_CHARS:
            colored_segments.append(with_style("".join(current_segment), style))
            current_segment.clear()
            colored_segments.append(char)
        else:
            current_segment.append(char)
    colored_segments.append(with_style("".join(current_segment), style))
    return "".join(colored_segments)


__all__ = ["call_method", "get_uninherited_methods", "create_function"]
