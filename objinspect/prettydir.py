from collections import defaultdict

from stdl.log import br
from stdl.st import colored

from objinspect import inspect
from objinspect._class import Class
from objinspect.function import Function
from objinspect.method import Method


def prettydir(
    obj: object,
    include_dunders: bool = False,
    color: bool = True,
    sep: bool = False,
    indent: int = 2,
) -> None:
    """
    Print the attributes and methods of an object in a pretty format.

    Args:
        obj (object): The object to be inspected.
        include_dunders (bool, optional): Whether to include dunder methods.
        color (bool, optional): Whether to colorize the output.
        sep (bool, optional): Whether to print a separator before and after the output.
        indent (int, optional): Indent width.
    """
    VARIABLE_SKIPS = [
        "__class__",
        "__dict__",
        "__weakref__",
        "__doc__",
        "__cached__",
        "__file__",
        "__loader__",
        "__builtins__",
        "__spec__",
        "__annotations__",
        "__module__",
    ]
    METHOD_SKIPS: list[str] = []

    def is_dunder(name: str) -> bool:
        return name.startswith("__") and name.endswith("__")

    if sep:
        br()

    data: defaultdict[str, dict[str, Function | Class | Method]] = defaultdict(dict)

    attrs = dir(obj)
    for attr_name in attrs:
        attr = getattr(obj, attr_name)
        try:
            inspected_obj = inspect(attr)
        except AttributeError:
            data["vars"][attr_name] = attr
            continue
        except Exception:
            continue

        if isinstance(inspected_obj, Function):
            if is_dunder(inspected_obj.name):
                data["dunders"][inspected_obj.name] = inspected_obj
            else:
                data["methods"][inspected_obj.name] = inspected_obj

    if include_dunders and len(data["dunders"].items()):
        print("Dunders:")
        for _, v in data["dunders"].items():
            print(" " * indent + v.as_str(color=color))

    variables = {k: v for k, v in data["vars"].items() if k not in VARIABLE_SKIPS}
    if len(variables):
        print("\nVariables:")
        for k, v in variables.items():
            k = colored(k, "light_blue") if color else k
            val_str = str(v)
            if isinstance(v, str):
                val_str = f"'{val_str}'"
            if len(val_str) > 50:
                val_str = val_str[:50] + "..."
            print(" " * indent + k + " = " + val_str)

    methods = {
        k: v for k, v in data["methods"].items() if k not in METHOD_SKIPS and isinstance(v, Method)
    }
    if len(methods):
        print("\nMethods:")
        for _, v in methods.items():
            print(" " * indent + v.as_str(color=color))

    functions = {
        k: v
        for k, v in data["methods"].items()
        if k not in METHOD_SKIPS and isinstance(v, Function)
    }
    if len(functions):
        print("\nFunctions:")
        for _, v in functions.items():
            print(" " * indent + v.as_str(color=color))
    if sep:
        br()


pdir = prettydir
