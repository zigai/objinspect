import inspect
from inspect import _ParameterKind

from objinspect.function import Function


class Method(Function):
    """
    The Method class represents a method of a class.

    Args:
        method (Callable): The method to be inspected.
        cls (type): The class to which the method belongs.
        skip_self (bool, optional): Whether to skip the self parameter. Defaults to True.

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

    def __init__(self, method, cls, skip_self: bool = True):
        super().__init__(method, skip_self)
        self.cls = cls

    @property
    def is_static(self) -> bool:
        for cls in inspect.getmro(self.cls):
            if inspect.isroutine(self.func):
                if self.name in cls.__dict__:
                    binded_value = cls.__dict__[self.name]
                    return isinstance(binded_value, staticmethod)
        return False

    @property
    def is_classmethod(self) -> bool:
        return hasattr(self.func, "__self__")

    @property
    def is_property(self) -> bool:
        return isinstance(getattr(self.cls, self.name), property)

    @property
    def is_private(self) -> bool:
        return self.name.startswith("_") and not self.name.startswith("__")

    @property
    def is_protected(self) -> bool:
        return self.name.startswith("_") and not self.name.endswith("__")

    @property
    def is_public(self) -> bool:
        return not self.is_private and not self.is_protected

    @property
    def is_inherited(self) -> bool:
        return self.name not in self.cls.__dict__


class MethodFilter:
    def __init__(
        self,
        init=True,
        public=True,
        inherited=True,
        static_methods=True,
        protected=False,
        private=False,
        classmethod=False,
    ) -> None:
        self.checks = []
        if not init:
            self.checks.append(lambda method: method.name == "__init__")
        if not static_methods:
            self.checks.append(lambda method: method.is_static)
        if not inherited:
            self.checks.append(lambda method: method.is_inherited)
        if not private:
            self.checks.append(lambda method: method.is_private)
        if not protected:
            self.checks.append(lambda method: method.is_protected)
        if not public:
            self.checks.append(lambda method: method.is_public)
        if not classmethod:
            self.checks.append(lambda method: method.is_classmethod)

    def check(self, method: Method) -> bool:
        for check_func in self.checks:
            if check_func(method):
                return False
        return True

    def extract(self, methods: list[Method]) -> list[Method]:
        return [i for i in methods if self.check(i)]


def split_args_kwargs(func_args: dict, func: Function | Method) -> tuple[tuple, dict]:
    """
    Split the arguments passed to a function into positional and keyword arguments.
    """
    args, kwargs = [], {}
    for param in func.params:
        if param.kind == _ParameterKind.POSITIONAL_ONLY:
            args.append(func_args[param.name])
        else:
            kwargs[param.name] = func_args[param.name]
    return tuple(args), kwargs


__all__ = ["Method", "MethodFilter"]
