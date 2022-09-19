import inspect

import docstring_parser

from interfacy_func import InterfacyFunction
from util import docstring_description, has_docstring


class InterfacyClass:
    def __init__(self, cls) -> None:
        self.cls = cls
        self.name: str = self.cls.__name__
        self.docstring = inspect.getdoc(self.cls)
        self.has_docstring = has_docstring(self.docstring)
        members = inspect.getmembers(self.cls, inspect.isfunction)
        self.has_init = members[0][0] == "__init__"
        self.methods = [InterfacyFunction(i[1]) for i in members]
        self.__parsed_docstring = self.__parse_docstring()
        self.description = docstring_description(self.__parsed_docstring)

    def __parse_docstring(self):
        return docstring_parser.parse(self.docstring) if self.has_docstring else None

    @property
    def dict(self):
        return {"name": self.name, "methods": [i.dict for i in self.methods]}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', methods={len(self.methods)}, has_init={self.has_init}, has_docstring={self.has_docstring})"
