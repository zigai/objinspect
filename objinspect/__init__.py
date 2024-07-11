import inspect as _inspect
from collections import defaultdict

from stdl.log import br
from stdl.st import colored

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
        protected (bool, optional): Whether to include protected attributes and methods (prefixed with _).
        private (bool, optional): Whether to include private attributes and methods (prefixed with __).

    Returns:
        An object representing the structure of the inspected object.


    Example:
    ``` python
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
    Function(name='inspect', parameters=7, description='Inspects an object and returns a structured representation of its attributes and methods.')
    ```
    """
    if _inspect.isclass(obj):
        return Class(
            obj,
            init=init,
            public=public,
            inherited=inherited,
            static_methods=static_methods,
            protected=protected,
            private=private,
        )
    if _inspect.ismethod(obj):
        return Method(obj, obj.__class__)
    return Function(obj)  # type: ignore


def prettydir(
    obj: object,
    dunders: bool = False,
    color: bool = True,
    sep: bool = False,
    indent: int = 2,
) -> None:
    """
    Print the attributes and methods of an object in a pretty format.

    Args:
        obj (object): The object to be inspected.
        dunders (bool, optional): Whether to include dunder methods.
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
    METHOD_SKIPS = []

    def is_dunder(name: str):
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

    if dunders and len(data["dunders"].items()):
        print("Dunders:")
        for k, v in data["dunders"].items():
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
        for k, v in methods.items():
            print(" " * indent + v.as_str(color=color))

    functions = {
        k: v
        for k, v in data["methods"].items()
        if k not in METHOD_SKIPS and isinstance(v, Function)
    }
    if len(functions):
        print("\nFunctions:")
        for k, v in functions.items():
            print(" " * indent + v.as_str(color=color))
    if sep:
        br()


pdir = prettydir

__all__ = [
    "inspect",
    "pdir",
    "prettydir",
    "Class",
    "Function",
    "Method",
    "Parameter",
    "MethodFilter",
]
