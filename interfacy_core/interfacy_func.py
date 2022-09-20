import inspect
from collections import OrderedDict
from typing import Callable, Iterable

import docstring_parser

from interfacy_core.interfacy_param import InterfacyParameter
from interfacy_core.util import docstring_description, has_docstring


class InterfacyFunction(Iterable):
    def __init__(self, func: Callable, owner: str | None = None) -> None:
        self.func = func
        self.name: str = self.func.__name__
        self.owner = owner
        self.docstring = inspect.getdoc(self.func)
        self.has_docstring = has_docstring(self.docstring)
        self.__parsed_docstr = self.__parse_docstring()
        self.parameters = self.__get_parameters()
        print(self.parameters)
        self.description = docstring_description(self.__parsed_docstr)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', parameters={len(self.parameters)}, owner={self.owner}, description={self.description})"

    def __iter__(self):
        for i in self.parameters.values():
            yield i

    def __getitem__(self, item: str | int) -> InterfacyParameter:
        match item:
            case str():
                return self.parameters[item]
            case int():
                return list(self.parameters.values())[item]
            case _:
                raise TypeError(type(item))

    def __parse_docstring(self):
        return docstring_parser.parse(self.docstring) if self.has_docstring else None

    def __get_parameters(self) -> OrderedDict[str, InterfacyParameter]:
        args = inspect.signature(self.func)
        params = [
            InterfacyParameter.from_inspect_param(i, owner=self.name)
            for i in args.parameters.values()
        ]
        # Try finding descriptions for parameters
        if self.has_docstring:
            docstr_params_map = {p.arg_name: p for p in self.__parsed_docstr.params}
            for param in params:
                if docstr_param := docstr_params_map.get(param.name, False):
                    if docstr_param.description:
                        param.description = docstr_param.description

        parameters = OrderedDict()
        for i in params:
            parameters[i.name] = i
        return parameters

    @property
    def dict(self):
        return {
            "name": self.name,
            "parameters": [i.dict for i in self.parameters.values()],
            "docstring": self.docstring,
        }
