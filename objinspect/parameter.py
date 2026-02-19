import inspect
from dataclasses import dataclass

from stdl.st import ForegroundColor, TextStyle, colored

from objinspect.constants import EMPTY
from objinspect.typing import type_name
from objinspect.util import colored_type

ParameterKind = type(inspect.Parameter.POSITIONAL_ONLY)


@dataclass
class ParameterStrTheme:
    name: ForegroundColor = "light_blue"
    type: ForegroundColor = "green"
    default: ForegroundColor = "blue"


class Parameter:
    """
    A `Parameter` instance contains information about a function or method parameter, including its name, type, default
    value, and description.
    """

    def __init__(
        self,
        name: str,
        kind: ParameterKind,
        annotation: object = EMPTY,
        default: object = EMPTY,
        description: str | None = None,
        infer_type: bool = True,
        **legacy_kwargs: object,
    ) -> None:
        """
        Initialize a `Parameter` instance.

        Args:
            name (str): The name of the parameter.
            kind: The kind of the parameter (e.g. POSITIONAL_ONLY, VAR_POSITIONAL).
            annotation (object): The type annotation of the parameter.
            default (object): The default value of the parameter.
            description (str | None): The description of the parameter.
            infer_type (bool): Infer the type of the parameter based on its default value.
            **legacy_kwargs (object): Backward-compatible keyword support for `type=`.
        """
        if "type" in legacy_kwargs:
            if annotation is not EMPTY:
                msg = "'annotation' and legacy 'type' cannot both be provided."
                raise TypeError(msg)
            annotation = legacy_kwargs.pop("type")
        if legacy_kwargs:
            unknown = ", ".join(sorted(legacy_kwargs))
            raise TypeError(f"Unexpected keyword arguments: {unknown}")

        self.name = name
        self.type = annotation
        self.default = default
        self.description = description
        self.kind = kind
        if infer_type and not self.is_typed:
            self.type = self.get_infered_type()

    def __repr__(self) -> str:
        data = f"name='{self.name}', kind={self.kind!s}, type={self.type}, default={self.default}, description='{self.description}'"
        return f"{self.__class__.__name__}({data})"

    def get_infered_type(self) -> object:
        """Infer the type of the parameter based on its default value."""
        if self.default is EMPTY:
            return EMPTY
        return type(self.default)

    @property
    def is_typed(self) -> bool:
        """Whether the parameter has an explicit type annotation."""
        return self.type is not EMPTY

    @property
    def is_required(self) -> bool:
        """Whether the parameter is required (has no default value)."""
        return self.default is EMPTY

    @property
    def is_optional(self) -> bool:
        """Whether the parameter is optional (has a default value)."""
        return not self.is_required

    @property
    def has_default(self) -> bool:
        """Whether the parameter has a default value."""
        return self.default is not EMPTY

    @property
    def dict(self) -> dict[str, object]:
        """Return a dictionary representation of the parameter."""
        return {
            "name": self.name,
            "kind": self.kind,
            "type": self.type,
            "default": self.default,
            "description": self.description,
        }

    def as_str(self, *, color: bool = True, theme: ParameterStrTheme | None = None) -> str:
        """
        Return a string representation of the parameter.

        Args:
            color (bool, optional): Whether to colorize the output.
            theme (ParameterStrTheme, optional): Color theme to use. Default will be used if None.
        """
        if theme is None:
            theme = ParameterStrTheme()

        if self.is_typed:
            if color:
                type_str = colored_type(self.type, style=TextStyle(theme.type), simplify=False)
            else:
                type_str = type_name(self.type)
        else:
            type_str = ""

        default_str = f"{self.default}" if self.is_optional else ""
        if self.default is not EMPTY:
            if color:
                default_str = colored(default_str, theme.default)
            default_str = f" = {default_str}"
        else:
            default_str = ""

        name_str = self.name if not color else colored(self.name, theme.name)
        return f"{name_str}{type_str}{default_str}"

    @classmethod
    def from_inspect_param(
        cls,
        param: inspect.Parameter,
        description: str | None = None,
    ) -> "Parameter":
        """
        Create a Parameter instance from an inspect.Parameter object.

        Args:
            param (inspect.Parameter): The inspect.Parameter to convert.
            description (str | None): Optional description for the parameter.
        """
        return cls(
            name=param.name,
            annotation=param.annotation,
            default=param.default,
            description=description,
            kind=param.kind,
        )


__all__ = ["Parameter"]
