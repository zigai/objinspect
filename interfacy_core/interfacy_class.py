import inspect
from collections import OrderedDict
from typing import Iterator

import docstring_parser

from interfacy_core.interfacy_func import InterfacyFunction
from interfacy_core.util import docstring_description, has_docstring


class InterfacyClass:
    def __init__(self, cls) -> None:
        self.cls = cls
        self.name: str = self.cls.__name__
        self.docstring = inspect.getdoc(self.cls)
        self.has_docstring = has_docstring(self.docstring)
        members = inspect.getmembers(self.cls, inspect.isfunction)
        methods = [InterfacyFunction(i[1]) for i in members]
        self.methods = OrderedDict()
        for i in methods:
            self.methods[i.name] = i
        self.has_init = "__init__" in self.methods
        self.__parsed_docstring = self.__parse_docstring()
        self.description = docstring_description(self.__parsed_docstring)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', methods={len(self.methods)}, has_init={self.has_init}, has_docstring={self.has_docstring})"

    def __iter__(self) -> Iterator[InterfacyFunction]:
        for i in self.methods.values():
            yield i

    def __getitem__(self, item: str | int) -> InterfacyFunction:
        match item:
            case str():
                return self.methods[item]
            case int():
                return list(self.methods.values())[item]
            case _:
                raise TypeError(type(item))

    def __parse_docstring(self):
        return docstring_parser.parse(self.docstring) if self.has_docstring else None

    @property
    def dict(self):
        return {"name": self.name, "methods": [i.dict for i in self.methods.values()]}
