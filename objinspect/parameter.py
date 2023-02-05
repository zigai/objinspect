import inspect
from typing import Any

from objinspect.constants import EMPTY


class Parameter:
    """
    A class to hold parameter information.

    A `Parameter` instance contains information about a function or method parameter, including its name, type, default
    value, and description.
    """

    def __init__(
        self,
        name: str,
        kind: inspect._ParameterKind,
        type: Any = EMPTY,
        default: Any = EMPTY,
        description: str | None = None,
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
        self._infer_type()

    def __repr__(self):
        data = f"name='{self.name}', kind={str(self.kind)}, type={self.type}, default={self.default}, description='{self.description}'"
        return f"{self.__class__.__name__}({data})"

    def _infer_type(self):
        """Infer the type of the parameter based on its default value."""
        if self.is_typed or self.is_required:
            return
        if self.default is None:
            return
        self.type = type(self.default)

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
