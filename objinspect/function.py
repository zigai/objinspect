import inspect
from types import NoneType
from typing import Any, Callable

import docstring_parser
from docstring_parser import Docstring

from objinspect.parameter import Parameter


def _has_docstr(docstring: str | None) -> bool:
    if docstring is None:
        return False
    return len(docstring) != 0


def _get_docstr_desc(docstring: Docstring | None) -> str:
    if docstring is None:
        return ""
    if docstring.short_description:
        return docstring.short_description
    if docstring.long_description:
        return docstring.long_description
    return ""


class Function:

    """
    A Function object represents a function and its attributes.

    Args:
        func (Callable): The function to be inspected.
        skip_self (bool, optional): Whether to skip the self parameter. Defaults to True.

    Attributes:
        name (str): The name of the function.
        docstring (str): The docstring of the function.
        has_docstring (bool): Whether the function has a docstring.
        description (str): The description part of the function's docstring.
        params (list[Parameter]): A list of parameters of the function.
        dict (dict): A dictionary representation of the function's attributes.

    """

    def __init__(self, func: Callable, skip_self: bool = True) -> None:
        self.func = func
        self.skip_self = skip_self
        self.name: str = self.func.__name__
        self.docstring = inspect.getdoc(self.func)
        self.has_docstring = _has_docstr(self.docstring)
        self._parsed_docstr: Docstring | None = (
            docstring_parser.parse(self.docstring) if self.has_docstring else None  # type: ignore
        )
        self.return_type = NoneType
        self._parameters = self._get_parameters()
        self.description = _get_docstr_desc(self._parsed_docstr)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', parameters={len(self._parameters)}, description='{self.description}')"

    def _get_parameters(self) -> dict[str, Parameter]:
        signature = inspect.signature(self.func)
        params = [Parameter.from_inspect_param(i) for i in signature.parameters.values()]
        self.return_type = signature.return_annotation

        # Try finding descriptions for parameters
        if self._parsed_docstr is not None:
            params_mapping = {par.arg_name: par for par in self._parsed_docstr.params}
            for param in params:
                if parameter := params_mapping.get(param.name, False):
                    if parameter.description:  # type: ignore
                        param.description = parameter.description  # type: ignore

        parameters = {}
        for param in params:
            if param.name == "self" and self.skip_self:
                continue
            parameters[param.name] = param
        return parameters

    def get_param(self, arg: str | int) -> Parameter:
        """
        Retrieve a single `Parameter` object.

        Args:
            arg (str | int): Either the name or index of the parameter to retrieve.

        Returns:
            Parameter: A `Parameter` object.

        Raises:
            TypeError: If arg is not a string or an integer.
        """
        match arg:
            case str():
                return self._parameters[arg]
            case int():
                return self.params[arg]
            case _:
                raise TypeError(type(arg))

    def call(self, *args, **kwargs) -> Any:
        """
        Calls the function and returns the result of its call.

        Args:
            *args: Positional arguments passed to the function.
            **kwargs: Keyword arguments passed to the function.
        """
        return self.func(*args, **kwargs)

    @property
    def params(self) -> list[Parameter]:
        """
        Returns a list of parameters of the function.
        """
        return list(self._parameters.values())

    @property
    def dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "parameters": [i.dict for i in self.params],
            "docstring": self.docstring,
        }


__all__ = ["Function"]
