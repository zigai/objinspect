import typing as T
from types import FunctionType

from objinspect.constants import EMPTY


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


__all__ = ["call_method", "get_uninherited_methods", "create_function"]
