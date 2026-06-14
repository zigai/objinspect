import inspect
from collections.abc import Callable
from inspect import _ParameterKind

from objinspect.function import Function
from objinspect.typing import RuntimeValue


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

    def __init__(
        self, method: Callable[..., RuntimeValue], cls: type, skip_self: bool = True
    ) -> None:
        super().__init__(method, skip_self)

        self.cls = cls

    def _lookup_descriptor(self) -> tuple[type, RuntimeValue] | tuple[None, None]:
        """Return the defining class and descriptor for this method, if found."""
        for cls in inspect.getmro(self.cls):
            candidate_names = [self.name]
            if self.is_private:
                candidate_names.append(f"_{cls.__name__.lstrip('_')}{self.name}")

            for candidate_name in candidate_names:
                if candidate_name in cls.__dict__:
                    return cls, cls.__dict__[candidate_name]

        return None, None

    @property
    def class_instance(self) -> RuntimeValue | None:
        """The instance to which this method is bound, or None if unbound."""
        return getattr(self.func, "__self__", None)

    @property
    def is_static(self) -> bool:
        """Whether the method is a static method."""
        if not inspect.isroutine(self.func):
            return False

        _, descriptor = self._lookup_descriptor()
        if descriptor is not None:
            return isinstance(descriptor, staticmethod)

        return False

    @property
    def is_classmethod(self) -> bool:
        """Whether the method is a class method."""
        _, descriptor = self._lookup_descriptor()
        if descriptor is not None:
            return isinstance(descriptor, classmethod)

        return False

    @property
    def is_property(self) -> bool:
        """Whether the method is a property."""
        _, descriptor = self._lookup_descriptor()
        return isinstance(descriptor, property)

    @property
    def is_private(self) -> bool:
        """Whether the method is private (double underscore prefix, excluding dunders)."""
        return self.name.startswith("__") and not self.name.endswith("__")

    @property
    def is_protected(self) -> bool:
        """Whether the method is protected (single underscore prefix, excluding dunders)."""
        return self.name.startswith("_") and not self.name.startswith("__")

    @property
    def is_public(self) -> bool:
        """Whether the method is public (no underscore prefix)."""
        return not self.name.startswith("_")

    @property
    def is_inherited(self) -> bool:
        """Whether the method is inherited from a parent class."""
        owner_cls, _ = self._lookup_descriptor()
        return owner_cls is not None and owner_cls is not self.cls


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
        filter_checks: tuple[tuple[bool, Callable[[Method], bool]], ...] = (
            (not init, lambda method: method.name == "__init__"),
            (not static_methods, lambda method: method.is_static),
            (not inherited, lambda method: method.is_inherited),
            (not private, lambda method: method.is_private),
            (not protected, lambda method: method.is_protected),
            (not public, lambda method: method.is_public),
            (not classmethod, lambda method: method.is_classmethod),
        )
        for enabled, check in filter_checks:
            if enabled:
                self.checks.append(check)

    def check(self, method: Method) -> bool:
        """
        Check if a method passes all filter criteria.

        Args:
            method (Method): The method to check.

        Returns:
            bool: True if the method passes all filters, False otherwise.
        """
        return all(not check_func(method) for check_func in self.checks)

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
    func_args: dict[str, RuntimeValue],
    func: Function | Method,
) -> tuple[tuple[RuntimeValue, ...], dict[str, RuntimeValue]]:
    """Split the arguments passed to a function into positional and keyword arguments."""
    args: list[RuntimeValue] = []
    kwargs: dict[str, RuntimeValue] = {}
    for param in func.params:
        if param.kind == _ParameterKind.POSITIONAL_ONLY:
            args.append(func_args[param.name])
        else:
            kwargs[param.name] = func_args[param.name]

    return tuple(args), kwargs


__all__ = ["Method", "MethodFilter", "split_args_kwargs"]
