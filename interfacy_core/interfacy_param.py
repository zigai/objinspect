import enum
import inspect
from typing import Any

from interfacy_core.constants import EMPTY


class ParameterShape(enum.IntEnum):
    BASIC = 1
    UNSUPPORTED = 2
    UNION = 3
    ALIAS = 4
    SPECIAL = 5


class InterfacyParameter:
    def __init__(
        self,
        name: str,
        kind: inspect._ParameterKind,
        type: Any = EMPTY,
        default: Any = EMPTY,
        description: str | None = None,
        owner: str | None = None,
    ) -> None:
        self.name = name
        self.type = type
        self.default = default
        self.description = description
        self.owner = owner
        self.kind = kind
        self.__infer_type()

    def __repr__(self):
        data = f"name={self.name}, type={self.type}, default={self.default}, owner={self.owner}, description='{self.description}'"
        return f"{self.__class__.__name__}({data})"

    @property
    def is_typed(self) -> bool:
        return self.type != EMPTY

    @property
    def is_required(self) -> bool:
        return self.default == EMPTY

    @property
    def is_optional(self) -> bool:
        return not self.is_required

    def __infer_type(self):
        if self.is_typed or self.is_required:
            return
        if self.default is None:
            return
        self.type = type(self.default)

    @property
    def dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "default": self.default,
            "description": self.description,
        }

    @classmethod
    def from_inspect_param(
        cls,
        param: inspect.Parameter,
        description: str | None = None,
        owner: str | None = None,
    ):
        return cls(
            name=param.name,
            type=param.annotation,
            default=param.default,
            description=description,
            kind=param.kind,
            owner=owner,
        )
