import inspect
from collections.abc import Callable
from dataclasses import dataclass
from types import NoneType
from typing import Any

import docstring_parser
from docstring_parser import Docstring
from stdl.st import ForegroundColor, ansi_ljust, colored

from objinspect.constants import EMPTY
from objinspect.parameter import Parameter
from objinspect.typing import type_name


def _has_docstr(docstring: str | None) -> bool:
    if docstring is None:
        return False
    return len(docstring) != 0


def _get_docstr_description(docstring: Docstring | None) -> str:
    if docstring is None:
        return ""
    if docstring.short_description:
        return docstring.short_description
    if docstring.long_description:
        return docstring.long_description
    return ""


@dataclass
class FunctionStrTheme:
    name: ForegroundColor = "yellow"
    bracket: ForegroundColor = "white"
    params: ForegroundColor = "light_blue"
    ret: ForegroundColor = "green"
    description: ForegroundColor = "gray"


class Function:
    """
    A Function object represents a function and its attributes.

    Args:
        func (Callable): The function to be inspected.
        skip_self (bool, optional): Whether to skip the self parameter.

    Attributes:
        name (str): The name of the function.
        docstring (Docstring | None): The parsed docstring object.
        docstring_text (str | None): The raw docstring text.
        has_docstring (bool): Whether the function has a docstring.
        description (str): The description part of the function's docstring.
        params (list[Parameter]): A list of parameters of the function.
        dict (dict): A dictionary representation of the function's attributes.

    """

    def __init__(self, func: Callable[..., Any], skip_self: bool = True) -> None:
        self.func = func
        self.skip_self = skip_self
        self.name: str = self.func.__name__
        self.docstring_text: str | None = inspect.getdoc(self.func)
        self.has_docstring = _has_docstr(self.docstring_text)
        self.docstring: Docstring | None = (
            docstring_parser.parse(self.docstring_text) if self.has_docstring else None  # type: ignore
        )
        self.return_type = NoneType
        self._parameters = self._get_parameters()
        self.description = _get_docstr_description(self.docstring)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', parameters={len(self._parameters)}, description='{self.description}')"

    def _get_parameters(self) -> dict[str, Parameter]:
        signature = inspect.signature(self.func)
        params = [Parameter.from_inspect_param(i) for i in signature.parameters.values()]
        self.return_type = signature.return_annotation

        if self.docstring is not None:
            params_mapping = {par.arg_name: par for par in self.docstring.params}
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

    def call(self, *args: Any, **kwargs: Any) -> Any:
        """
        Calls the function and returns the result of its call.

        Args:
            *args: Positional arguments passed to the function.
            **kwargs: Keyword arguments passed to the function.
        """
        return self.func(*args, **kwargs)

    @property
    def params(self) -> list[Parameter]:
        """Returns a list of parameters of the function."""
        return list(self._parameters.values())

    @property
    def dict(self) -> dict[str, Any]:
        """Return a dictionary representation of the function."""
        return {
            "name": self.name,
            "parameters": [i.dict for i in self.params],
            "docstring": self.docstring_text,
        }

    @property
    def is_coroutine(self) -> bool:
        """Whether the function is a coroutine (async function)."""
        return inspect.iscoroutinefunction(self.func)

    def as_str(
        self,
        *,
        color: bool = True,
        description: bool = True,
        ljust: int = 58,
        theme: FunctionStrTheme | None = None,
    ) -> str:
        """
        Return a string representation of the function.

        Args:
            color (bool, optional): Whether to colorize the string.
            description (bool, optional): Whether to include the description of the function.
            ljust (int, optional): The width of the string.
            theme (FunctionStrTheme, optional): Color theme to use. Default will be used if None.

        """
        if theme is None:
            theme = FunctionStrTheme()

        name_str: str = self.name if not color else colored(self.name, theme.name)
        params: str = ", ".join([i.as_str(color=color) for i in self.params])
        if color:
            params = colored("(", theme.bracket) + params + colored(")", theme.bracket)

        if self.return_type is not EMPTY and self.return_type is not None:  # type: ignore[comparison-overlap]
            return_str: str = type_name(self.return_type)
            if color:
                return_str = colored(return_str, theme.ret)
            return_str = " -> " + return_str
        else:
            return_str = ""

        string: str = f"{name_str}{params}{return_str}"

        if description and self.description:
            string = ansi_ljust(string, ljust)
            description_str = f" # {self.description}"
            if color:
                description_str = colored(description_str, theme.description)
            string += description_str
            return string
        return string


__all__ = ["Function"]
