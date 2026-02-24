import inspect
from collections.abc import Callable
from types import FunctionType
from typing import cast

from stdl.st import TextStyle, with_style

from objinspect.constants import EMPTY
from objinspect.typing import simplified_type_name, type_name


def call_method(
    obj: object,
    name: str,
    args: tuple[object, ...] = (),
    kwargs: dict[str, object] | None = None,
) -> object:
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


async def call_method_async(
    obj: object,
    name: str,
    args: tuple[object, ...] = (),
    kwargs: dict[str, object] | None = None,
) -> object:
    """
    Call a method with the given name on the given object and await when needed.

    Args:
        obj (object): The object to call the method on.
        name (str): The name of the method to call.
        args (tuple, optional): The positional arguments to pass to the method.
        kwargs (dict, optional): The keyword arguments to pass to the method.

    Returns:
        object: The result of calling the method.
    """
    kwargs = kwargs or {}
    result = getattr(obj, name)(*args, **kwargs)
    if inspect.isawaitable(result):
        return await result
    return result


def get_uninherited_methods(cls: type) -> list[str]:
    """Get the methods of a class that are not inherited from its parent classes."""
    return [
        name
        for name, method in cls.__dict__.items()
        if isinstance(method, (FunctionType, classmethod, staticmethod))
    ]


ArgumentDef = tuple[object] | tuple[object, object]


def _parse_argument_def(name: str, arg_def: ArgumentDef) -> tuple[object, object]:
    if len(arg_def) == 2:
        return arg_def
    if len(arg_def) == 1:
        return arg_def[0], EMPTY
    raise ValueError(f"Invalid annotations for argument {name}: {arg_def}")


def _build_argument_signature(args: dict[str, ArgumentDef]) -> str:
    arg_str: list[str] = []
    for arg_name, arg_def in args.items():
        arg_type, default = _parse_argument_def(arg_name, arg_def)
        if arg_type is EMPTY:
            arg_repr = arg_name
        elif isinstance(arg_type, type):
            arg_repr = f"{arg_name}: {arg_type.__name__}"
        else:
            arg_repr = f"{arg_name}: {type_name(arg_type)}"
        if default is not EMPTY:
            arg_repr += f" = {default!r}"
        arg_str.append(arg_repr)
    return ", ".join(arg_str)


def _build_return_signature(return_type: object) -> str:
    if return_type is EMPTY:
        return ""
    if return_type is None:
        return " -> None"
    if hasattr(return_type, "__name__"):
        return f" -> {return_type.__name__}"
    return ""


def _build_function_source(
    *,
    name: str,
    args: dict[str, ArgumentDef],
    body: str | list[str],
    return_type: object,
    docstring: str | None,
) -> str:
    arg_str_final = _build_argument_signature(args)
    body_str = "\n    ".join(body) if isinstance(body, list) else body
    function_source = f"def {name}({arg_str_final})"
    function_source += _build_return_signature(return_type)
    function_source += ":"
    if docstring:
        function_source += f'\n    """{docstring}"""'
    function_source += f"\n    {body_str}"
    return function_source


def create_function(
    name: str,
    args: dict[str, ArgumentDef],
    body: str | list[str],
    globs: dict[str, object],
    return_type: object = EMPTY,
    docstring: str | None = None,
) -> Callable[..., object]:
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
    func_str = _build_function_source(
        name=name,
        args=args,
        body=body,
        return_type=return_type,
        docstring=docstring,
    )
    code_obj = compile(func_str, "<string>", "exec")
    exec(code_obj, globs)  # noqa: S102  # required for runtime function definition
    func = cast(Callable[..., object], globs[name])
    func.__annotations__ = {arg: annotation[0] for arg, annotation in args.items()}
    if return_type is not EMPTY:
        func.__annotations__["return"] = return_type

    return func


def colored_type(
    t: object,
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


__all__ = ["call_method", "call_method_async", "create_function", "get_uninherited_methods"]
