import inspect
from collections import OrderedDict
from typing import Any

import docstring_parser

from objinspect.function import _get_docstr_desc, _has_docstr
from objinspect.method import Method
from objinspect.method_extractor import MethodExtractor


class Class:
    def __init__(
        self,
        cls,
        init=True,
        public=True,
        inherited=True,
        static_methods=True,
        protected=False,
        private=False,
    ) -> None:
        self.cls = cls
        self.is_initialized = False
        try:
            self.name: str = self.cls.__name__
        except AttributeError:
            self.name = f"{self.cls.__class__.__name__} instance"
            self.is_initialized = True
        self.instance = None if not self.is_initialized else self.cls
        self.docstring = inspect.getdoc(self.cls)
        self.has_docstring = _has_docstr(self.docstring)
        self.extractor_kwargs = {
            "init": init,
            "public": public,
            "inherited": inherited,
            "static_methods": static_methods,
            "protected": protected,
            "private": private,
        }
        self._methods = self._find_methods()
        self.has_init = "__init__" in self._methods
        self._parsed_docstring = (
            docstring_parser.parse(self.docstring) if self.has_docstring else None
        )
        self.description = _get_docstr_desc(self._parsed_docstring)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', methods={len(self._methods)}, has_init={self.has_init}, description={self.description})"

    def _get_class_base(self):
        if self.is_initialized:
            return self.cls.__class__
        return self.cls

    def _find_methods(self):
        methods = OrderedDict()
        for i in MethodExtractor(**self.extractor_kwargs).extract(self._get_class_base()):
            methods[i.name] = i
        return methods

    def initialize(self, *args, **kwargs) -> None:
        if self.is_initialized:
            raise ValueError(f"Class {self.cls} is already initialized")
        self.instance = self.cls(*args, **kwargs)
        self.is_initialized = True

    def call_method(self, method: str | int, *args, **kwargs) -> Any:
        if not self.is_initialized:
            raise ValueError("Class is not initialized")
        return self.get_method(method).call(self.instance, *args, **kwargs)

    def get_method(self, method: str | int) -> Method:
        """
        Retrieves a method from the list of methods of the class or instance.

        Args:
            method (str | int): The method name or index to retrieve.

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
    def methods(self) -> list[Method]:
        """
        Returns the list of methods of the class or instance as a list of :class:`Function` objects.
        """
        return list(self._methods.values())

    @property
    def dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "methods": [i.dict for i in self.methods],
            "description": self.description,
            "initialized": self.is_initialized,
        }


__all__ = ["Class"]
