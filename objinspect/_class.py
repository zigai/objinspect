import functools
import inspect
from dataclasses import dataclass
from typing import Any

import docstring_parser
from docstring_parser import Docstring
from stdl.st import ForegroundColor, colored

from objinspect.function import _get_docstr_description, _has_docstr
from objinspect.method import Method, MethodFilter
from objinspect.parameter import Parameter


@dataclass
class ClassStrTheme:
    class_kw: ForegroundColor = "blue"
    name: ForegroundColor = "yellow"
    description: ForegroundColor = "gray"


class Class:
    """
    Wraps  a class or class instance and provides information about its methods.

    Args:
        cls (type or object): The class or class instance to wrap.
        init (bool, optional): Include the class's __init__ method.
        public (bool, optional): Include public methods.
        inherited (bool, optional): Include inherited methods.
        static_methods (bool, optional): Include static methods.
        classmethod (bool, optional): Include class methods.
        protected (bool, optional): Include protected methods.
        private (bool, optional): Include private methods.

    Attributes:
        cls (type or object): The class or class instance that was passed as an argument.
        is_initialized (bool): Whether the class has been initialized as an instance.
        name (str): The name of the class.
        instance (object | None): The instance of the class if it has been initialized, otherwise None.
        docstring (Docstring | None): The parsed docstring object.
        docstring_text (str | None): The raw docstring text.
        has_docstring (bool): Whether the class has a docstring.
        extractor_kwargs (dict): The keyword arguments used to initialize the MethodExtractor object.
        has_init (bool): Whether the class has an __init__ method.
        description (str): The description of the class from its docstring.
    """

    def __init__(
        self,
        cls: type | object,
        init: bool = True,
        public: bool = True,
        inherited: bool = True,
        static_methods: bool = True,
        protected: bool = False,
        private: bool = False,
        classmethod: bool = True,
        skip_self: bool = True,
    ) -> None:
        self.cls = cls
        self.skip_self = skip_self
        self.receieved_instance = not inspect.isclass(cls)

        if self.receieved_instance:
            self.is_initialized = True
            self.instance = cls
            self.name = f"{cls.__class__.__name__} instance"
        else:
            self.is_initialized = False
            self.instance = None
            self.name = getattr(cls, "__name__", str(cls))
        self.docstring_text: str | None = inspect.getdoc(self.cls)
        self.has_docstring = _has_docstr(self.docstring_text)
        self.extractor_kwargs = {
            "init": init,
            "public": public,
            "inherited": inherited,
            "static_methods": static_methods,
            "protected": protected,
            "private": private,
            "classmethod": classmethod,
        }
        self._methods = self._find_methods()
        self.has_init = "__init__" in self._methods
        self.docstring: Docstring | None = (
            docstring_parser.parse(self.docstring_text) if self.has_docstring else None  # type: ignore
        )
        self.description = _get_docstr_description(self.docstring)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', methods={len(self._methods)}, has_init={self.has_init}, description={self.description})"

    @functools.cached_property
    def _class_base(self) -> type:
        if self.is_initialized:
            return self.cls.__class__ if hasattr(self.cls, "__class__") else type(self.cls)
        return self.cls  # type: ignore[return-value]

    def _find_methods(self) -> dict[str, Method]:
        method_filter = MethodFilter(**self.extractor_kwargs)
        if self.is_initialized:
            members = inspect.getmembers(self.cls, inspect.ismethod)
        else:
            members = inspect.getmembers(
                self.cls, lambda m: inspect.isfunction(m) or inspect.ismethod(m)
            )
        methods = {}
        for method in method_filter.extract(
            [Method(i[1], self._class_base, skip_self=self.skip_self) for i in members]
        ):
            methods[method.name] = method
        return methods

    def init(self, *args: Any, **kwargs: Any) -> None:
        """
        Initializes the class as an instance using the provided arguments.

        Raises:
            ValueError: If the class is already initialized.

        """
        if self.is_initialized:
            raise ValueError(f"Class {self.cls} is already initialized")
        if callable(self.cls):
            self.instance = self.cls(*args, **kwargs)
        else:
            raise TypeError(f"Cannot initialize object of type {type(self.cls)}")
        self.is_initialized = True

    def call_method(self, method: str | int, *args: Any, **kwargs: Any) -> Any:
        """
        Calls the specified method on the class or instance.

        Args:
            method (str | int): The name or index of the method to call.
            *args: Positional arguments to pass to the method.
            **kwargs: Keyword arguments to pass to the method.

        Returns:
            Any: The result of calling the specified method.

        Raises:
            ValueError: If the class has not been initialized.
        """
        method_obj = self.get_method(method)
        if not self.is_initialized and not method_obj.is_static:
            raise ValueError(f"Class {self.cls} is not initialized")
        if self.receieved_instance:
            return method_obj.call(*args, **kwargs)
        return method_obj.call(self.instance, *args, **kwargs)

    def get_method(self, method: str | int) -> Method:
        """
        Retrieves a method from the list of methods of the class or instance.

        Args:
            method (str | int): The method name or index to retrieve.

        Returns:
            Method: The `Method` object representing the requested method.
        """
        match method:
            case str():
                return self._methods[method]
            case int():
                return self.methods[method]
            case _:
                raise TypeError(type(method))

    @property
    def init_method(self) -> Method | None:
        """The __init__ method of the class, or None if not present."""
        try:
            return self.get_method("__init__")
        except KeyError:
            return None

    @property
    def init_args(self) -> list[Parameter] | None:
        """The parameters of the __init__ method, or None if not present."""
        if self.init_method is None:
            return None
        return self.init_method.params

    @property
    def methods(self) -> list[Method]:
        """Returns the list of methods of the class or instance as a list of :class:`Function` objects."""
        return list(self._methods.values())

    @property
    def dict(self) -> dict[str, Any]:
        """Return a dictionary representation of the class."""
        return {
            "name": self.name,
            "methods": [method.dict for method in self.methods],
            "description": self.description,
            "initialized": self.is_initialized,
            "docstring": self.docstring_text,
        }

    def as_str(
        self,
        *,
        color: bool = True,
        indent: int = 2,
        theme: ClassStrTheme | None = None,
    ) -> str:
        """
        Return a string representation of the class.

        Args:
            color (bool, optional): Whether to colorize the output. Defaults to True.
            indent (int, optional): Indentation width for methods. Defaults to 2.
            theme (ClassStrTheme | None): Color theme to use. Default will be used if
                None.
        """
        if theme is None:
            theme = ClassStrTheme()

        string: str
        if color:
            string = colored("class", theme.class_kw) + " " + colored(self.name, theme.name) + ":"
        else:
            string = f"class {self.name}:"

        if self.description:
            if color:
                string += "\n" + colored(self.description, theme.description)
            else:
                string += "\n" + str(self.description)
        if not len(self.methods):
            return string

        string += "\n"
        string += "\n".join([" " * indent + method.as_str(color=color) for method in self.methods])
        return string


def split_init_args(
    args: dict[str, Any],
    cls: Class,
    method: Method,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Split the arguments into those that should be passed to the __init__ method
    and those that should be passed to the method call.
    """
    if not method.is_static and cls.has_init:
        init_method = cls.get_method("__init__")
        init_arg_names = [i.name for i in init_method.params]
        args_init = {k: v for k, v in args.items() if k in init_arg_names}
        args_method = {k: v for k, v in args.items() if k not in init_arg_names}
        return args_init, args_method
    return {}, args


__all__ = ["Class", "split_init_args"]
