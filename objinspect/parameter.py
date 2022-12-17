import inspect
from typing import Any

from objinspect.constants import EMPTY


class Parameter:
    def __init__(
        self,
        name: str,
        kind: inspect._ParameterKind,
        type: Any = EMPTY,
        default: Any = EMPTY,
        description: str | None = None,
    ) -> None:
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
