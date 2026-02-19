from collections import defaultdict

from stdl.log import br
from stdl.st import colored

from objinspect import inspect
from objinspect._class import Class
from objinspect.function import Function
from objinspect.method import Method

VARIABLE_SKIPS = {
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
}
METHOD_SKIPS: set[str] = set()


def _is_dunder(name: str) -> bool:
    return name.startswith("__") and name.endswith("__")


def _try_inspect_attribute(attr: object) -> tuple[Function | Class | Method | None, bool]:
    try:
        return inspect(attr), False
    except AttributeError:
        return None, True
    except (TypeError, ValueError):
        return None, False


def _collect_data(obj: object) -> defaultdict[str, dict[str, object]]:
    data: defaultdict[str, dict[str, object]] = defaultdict(dict)
    for attr_name in dir(obj):
        try:
            attr = getattr(obj, attr_name)
        except AttributeError:
            continue

        inspected_obj, is_variable = _try_inspect_attribute(attr)
        if is_variable:
            data["vars"][attr_name] = attr
            continue
        if not isinstance(inspected_obj, Function):
            continue

        key = "dunders" if _is_dunder(inspected_obj.name) else "methods"
        data[key][inspected_obj.name] = inspected_obj
    return data


def _format_variable_value(value: object) -> str:
    value_str = f"'{value}'" if isinstance(value, str) else str(value)
    if len(value_str) > 50:
        return value_str[:50] + "..."
    return value_str


def _print_dunders(
    dunders: dict[str, object], *, include_dunders: bool, color: bool, indent: int
) -> None:
    if not include_dunders or not dunders:
        return

    print("Dunders:")
    for dunder in dunders.values():
        if isinstance(dunder, Function):
            print(" " * indent + dunder.as_str(color=color))


def _print_variables(variables: dict[str, object], *, color: bool, indent: int) -> None:
    visible_vars = {key: value for key, value in variables.items() if key not in VARIABLE_SKIPS}
    if not visible_vars:
        return

    print("\nVariables:")
    for key, value in visible_vars.items():
        visible_key = colored(key, "light_blue") if color else key
        print(" " * indent + visible_key + " = " + _format_variable_value(value))


def _collect_methods_of_type(
    members: dict[str, object],
    method_type: type[Function],
) -> list[Function]:
    return [
        member
        for member_name, member in members.items()
        if member_name not in METHOD_SKIPS and isinstance(member, method_type)
    ]


def _print_function_like_section(
    title: str,
    methods: list[Function],
    *,
    color: bool,
    indent: int,
) -> None:
    if not methods:
        return

    print(f"\n{title}:")
    for method in methods:
        print(" " * indent + method.as_str(color=color))


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
    if sep:
        br()

    data = _collect_data(obj)
    _print_dunders(data["dunders"], include_dunders=include_dunders, color=color, indent=indent)
    _print_variables(data["vars"], color=color, indent=indent)
    _print_function_like_section(
        "Methods",
        _collect_methods_of_type(data["methods"], Method),
        color=color,
        indent=indent,
    )
    _print_function_like_section(
        "Functions",
        _collect_methods_of_type(data["methods"], Function),
        color=color,
        indent=indent,
    )
    if sep:
        br()


pdir = prettydir
