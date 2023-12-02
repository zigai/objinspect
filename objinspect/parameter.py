import inspect
import typing as T

from stdl.st import colored

from objinspect.constants import EMPTY
from objinspect.util import type_to_str

ParameterKind = inspect._ParameterKind


class Parameter:
    """
    A `Parameter` instance contains information about a function or method parameter, including its name, type, default
    value, and description.
    """

    def __init__(
        self,
        name: str,
        kind: ParameterKind,
        type: T.Any = EMPTY,
        default: T.Any = EMPTY,
        description: str | None = None,
        infer_type: bool = True,
    ) -> None:
        """
        Initialize a `Parameter` instance.

        Args:
            name (str): The name of the parameter.
            kind (inspect._ParameterKind): The kind of the parameter, i.e. POSITIONAL_ONLY, POSITIONAL_OR_KEYWORD, VAR_POSITIONAL,
                KEYWORD_ONLY, or VAR_KEYWORD.
            type (Any): The type of the parameter.
            default (Any): The default value of the parameter.
            description (str | None): The description of the parameter.
        """
        self.name = name
        self.type = type
        self.default = default
        self.description = description
        self.kind = kind
        if infer_type and not self.is_typed:
            self.type = self.get_infered_type()

    def __repr__(self):
        data = f"name='{self.name}', kind={str(self.kind)}, type={self.type}, default={self.default}, description='{self.description}'"
        return f"{self.__class__.__name__}({data})"

    def get_infered_type(self):
        """Infer the type of the parameter based on its default value."""
        if self.default is EMPTY:
            return EMPTY
        return type(self.default)

    @property
    def is_typed(self) -> bool:
        return self.type != EMPTY

    @property
    def is_required(self) -> bool:
        return self.default == EMPTY

    @property
    def is_optional(self) -> bool:
        return not self.is_required

    @property
    def dict(self):
        return {
            "name": self.name,
            "kind": self.kind,
            "type": self.type,
            "default": self.default,
            "description": self.description,
        }

    def to_str(self, *, color: bool = True) -> str:
        """
        Return a string representation of the parameter.

        Args:
            color (bool, optional): Whether to colorize the output. Defaults to True.
        """
        type_str = f"{type_to_str(self.type)}" if self.is_typed else ""
        if color and type_str:
            type_str = colored(type_str, "green")
        type_str = f": {type_str}" if type_str != "" else ""

        default_str = f"{self.default}" if self.is_optional else ""
        if self.default is not EMPTY:
            if color:
                default_str = colored(default_str, "blue")
            default_str = f" = {default_str}"
        else:
            default_str = ""
        name_str = self.name if not color else colored(self.name, "light_blue")
        return f"{name_str}{type_str}{default_str}"

    @classmethod
    def from_inspect_param(
        cls,
        param: inspect.Parameter,
        description: str | None = None,
    ):
        return cls(
            name=param.name,
            type=param.annotation,
            default=param.default,
            description=description,
            kind=param.kind,
        )


__all__ = ["Parameter"]
