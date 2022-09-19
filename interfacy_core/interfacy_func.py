import inspect
from typing import Callable

import docstring_parser

from interfacy_core.interfacy_param import InterfacyParameter
from interfacy_core.util import docstring_description, has_docstring


class InterfacyFunction:
    def __init__(self, func: Callable, owner: str | None = None) -> None:
        self.func = func
        self.name: str = self.func.__name__
        self.owner = owner
        self.docstring = inspect.getdoc(self.func)
        self.has_docstring = has_docstring(self.docstring)
        self.__parsed_docstr = self.__parse_docstring()
        self.parameters = self.__get_parameters()
        self.description = docstring_description(self.__parsed_docstr)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', parameters={len(self.parameters)}, owner={self.owner}, description={self.description})"

    def __parse_docstring(self):
        return docstring_parser.parse(self.docstring) if self.has_docstring else None

    def __get_parameters(self):
        args = inspect.signature(self.func)
        parameters = [
            InterfacyParameter.from_inspect_param(i, owner=self.name)
            for i in args.parameters.values()
        ]

        # Try finding descriptions for parameters
        if self.has_docstring:
            params_mapping = {p.arg_name: p for p in self.__parsed_docstr.params}
            for param in parameters:
                if docstr_param := params_mapping.get(param.name, False):
                    if docstr_param.description:
                        param.description = docstr_param.description
        return parameters

    @property
    def dict(self):
        return {
            "name": self.name,
            "parameters": [i.dict for i in self.parameters],
            "docstring": self.docstring,
        }
