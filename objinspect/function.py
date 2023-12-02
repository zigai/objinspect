import inspect
import typing as T
from types import NoneType

import docstring_parser
from docstring_parser import Docstring
from stdl.st import ansi_ljust, colored

from objinspect.constants import EMPTY
from objinspect.parameter import Parameter
from objinspect.util import type_to_str


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

    def __init__(self, func: T.Callable, skip_self: bool = True) -> None:
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

    def call(self, *args, **kwargs) -> T.Any:
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
    def dict(self) -> dict[str, T.Any]:
        return {
            "name": self.name,
            "parameters": [i.dict for i in self.params],
            "docstring": self.docstring,
        }

    def to_str(self, *, color: bool = True, description: bool = True, ljust: int = 58) -> str:
        """
        Return a string representation of the function.

        Args:
            color (bool, optional): Whether to colorize the string. Defaults to True.
            description (bool, optional): Whether to include the description of the function. Defaults to True.
            ljust (int, optional): The width of the string. Defaults to 50.
        """
        name_str = self.name if not color else colored(self.name, "yellow")
        params = ", ".join([i.to_str(color=color) for i in self.params])
        if color:
            params = colored("(", "yellow") + params + colored(")", "yellow")

        if self.return_type is not EMPTY:
            return_str = type_to_str(self.return_type)
            if color:
                return_str = colored(return_str, "green")
            return_str = " -> " + return_str
        else:
            return_str = ""

        string = f"{name_str}{params}{return_str}"

        if description and self.description:
            string = ansi_ljust(string, ljust)
            description_str = f" # {self.description}"
            if color:
                description_str = colored(description_str, "gray")
            return string + description_str
        return string


__all__ = ["Function"]
