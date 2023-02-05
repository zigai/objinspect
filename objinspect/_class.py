import inspect
from collections import OrderedDict

import docstring_parser

from objinspect.function import Function, _get_docstr_desc, _has_docstr
from objinspect.util import get_methods


class Class:
    """
    The Class inspects a class or an instance of a class and provides access to the class's methods and other information about the class.

    Args:
        cls (class or instance): The class to be inspected.
        include_inherited (bool, optional): If set to True, the class's inherited methods will also be inspected. Default is True.

    Attributes:
        name (str): The name of the class or instance.
        docstring (str): The docstring of the class or instance, if present.
        has_docstring (bool): Whether the class or instance has a docstring or not.
        methods (list[Function]): A list of :class:`objinspect.function.Function` objects representing the class's methods.
        has_init (bool): Whether the class has an `__init__` method or not.
        description (str): The first line of the class's docstring, if present.
        dict (dict): A dictionary representation of the class, containing 'name', 'methods'.
    """

    def __init__(self, cls, include_inherited: bool = True) -> None:
        self.cls = cls
        self.include_inherited = include_inherited
        self.initialized = False
        try:
            self.name: str = self.cls.__name__
        except AttributeError:
            self.name = f"{self.cls.__class__.__name__} instance"
            self.initialized = True

        self.docstring = inspect.getdoc(self.cls)
        self.has_docstring = _has_docstr(self.docstring)
        self._methods = self._find_methods()
        self.has_init = "__init__" in self._methods
        self._parsed_docstring = (
            docstring_parser.parse(self.docstring) if self.has_docstring else None
        )
        self.description = _get_docstr_desc(self._parsed_docstring)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', methods={len(self._methods)}, has_init={self.has_init}, has_docstring={self.has_docstring})"

    def _find_methods(self):
        if self.initialized:
            members = inspect.getmembers(self.cls, inspect.ismethod)
        else:
            members = inspect.getmembers(self.cls, inspect.isfunction)
        if not self.include_inherited:
            if not self.initialized:
                members = [i for i in members if i[0] in get_methods(self.cls)]
            else:
                members = [i for i in members if i[0] in get_methods(self.cls.__class__)]
        methods = OrderedDict()
        for i in [Function(i[1]) for i in members]:
            methods[i.name] = i
        return methods

    def get_method(self, method: str | int):
        """
        Retrieves a method from the list of methods of the class or instance.

        Args:
            method (str or int): The method name or index to retrieve.

        Returns:
            Function: The :class:`Function` object representing the requested method.
        """
        match method:
            case str():
                return self._methods[method]
            case int():
                return self.methods[method]
            case _:
                raise TypeError(type(method))

    @property
    def methods(self) -> list[Function]:
        """
        Returns the list of methods of the class or instance as a list of :class:`Function` objects.
        """
        return list(self._methods.values())

    @property
    def dict(self):
        return {"name": self.name, "methods": [i.dict for i in self._methods.values()]}


__all__ = ["Class"]
