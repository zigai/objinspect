import inspect
from collections.abc import Callable
from inspect import _ParameterKind
from typing import Any

from objinspect.function import Function


class Method(Function):
    """
    The Method class represents a method of a class.

    Args:
        method (Callable): The method to be inspected.
        cls (type): The class to which the method belongs.
        skip_self (bool, optional): Whether to skip the self parameter.

    Attributes:
        name (str): The name of the method.
        docstring (str): The docstring of the method.
        has_docstring (bool): Whether the method has a docstring.
        description (str): The description part of the method's docstring.
        params (list[Parameter]): A list of parameters of the method.
        dict (dict): A dictionary representation of the method's attributes.
        is_static (bool): Whether the method is static.
        is_classmethod (bool): Whether the method is a classmethod.
        is_property (bool): Whether the method is a property.
        is_private (bool): Whether the method is private.
        is_protected (bool): Whether the method is protected.
        is_public (bool): Whether the method is public.
        is_inherited (bool): Whether the method is inherited.

    """

    def __init__(self, method: Callable[..., Any], cls: type, skip_self: bool = True) -> None:
        super().__init__(method, skip_self)
        self.cls = cls

    @property
    def class_instance(self) -> object | None:
        """The instance to which this method is bound, or None if unbound."""
        return getattr(self.func, "__self__", None)

    @property
    def is_static(self) -> bool:
        """Whether the method is a static method."""
        for cls in inspect.getmro(self.cls):
            if inspect.isroutine(self.func):
                if self.name in cls.__dict__:
                    binded_value = cls.__dict__[self.name]
                    return isinstance(binded_value, staticmethod)
        return False

    @property
    def is_classmethod(self) -> bool:
        """Whether the method is a class method."""
        for cls in inspect.getmro(self.cls):
            if self.name in cls.__dict__:
                return isinstance(cls.__dict__[self.name], classmethod)
        return False

    @property
    def is_property(self) -> bool:
        """Whether the method is a property."""
        return isinstance(getattr(self.cls, self.name), property)

    @property
    def is_private(self) -> bool:
        """Whether the method is private (single underscore prefix)."""
        return self.name.startswith("_") and not self.name.startswith("__")

    @property
    def is_protected(self) -> bool:
        """Whether the method is protected (single underscore prefix and suffix)."""
        return self.name.startswith("_") and not self.name.endswith("__")

    @property
    def is_public(self) -> bool:
        """Whether the method is public (no underscore prefix)."""
        return not self.is_private and not self.is_protected

    @property
    def is_inherited(self) -> bool:
        """Whether the method is inherited from a parent class."""
        return self.name not in self.cls.__dict__


class MethodFilter:
    def __init__(
        self,
        init: bool = True,
        public: bool = True,
        inherited: bool = True,
        static_methods: bool = True,
        protected: bool = False,
        private: bool = False,
        classmethod: bool = False,
    ) -> None:
        self.checks: list[Callable[[Method], bool]] = []
        # fmt: off
        if not init: self.checks.append(lambda method: method.name == "__init__")
        if not static_methods: self.checks.append(lambda method: method.is_static)
        if not inherited: self.checks.append(lambda method: method.is_inherited)
        if not private: self.checks.append(lambda method: method.is_private)
        if not protected: self.checks.append(lambda method: method.is_protected)
        if not public: self.checks.append(lambda method: method.is_public)
        if not classmethod: self.checks.append(lambda method: method.is_classmethod)
        # fmt: on

    def check(self, method: Method) -> bool:
        """
        Check if a method passes all filter criteria.

        Args:
            method (Method): The method to check.

        Returns:
            bool: True if the method passes all filters, False otherwise.
        """
        for check_func in self.checks:
            if check_func(method):
                return False
        return True

    def extract(self, methods: list[Method]) -> list[Method]:
        """
        Filter a list of methods based on the configured criteria.

        Args:
            methods (list[Method]): The list of methods to filter.

        Returns:
            list[Method]: The filtered list of methods.
        """
        return [i for i in methods if self.check(i)]


def split_args_kwargs(
    func_args: dict[str, object],
    func: Function | Method,
) -> tuple[tuple[object, ...], dict[str, object]]:
    """Split the arguments passed to a function into positional and keyword arguments."""
    args: list[object] = []
    kwargs: dict[str, object] = {}
    for param in func.params:
        if param.kind == _ParameterKind.POSITIONAL_ONLY:
            args.append(func_args[param.name])
        else:
            kwargs[param.name] = func_args[param.name]
    return tuple(args), kwargs


__all__ = ["Method", "MethodFilter", "split_args_kwargs"]
