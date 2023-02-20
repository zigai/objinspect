import inspect
import types

from objinspect.function import Function


class Method(Function):
    def __init__(self, func, cls, skip_self: bool = True):
        super().__init__(func, skip_self)
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
        return not self.name in self.cls.__dict__


class MethodFilter:
    def __init__(
        self,
        init=True,
        public=True,
        inherited=True,
        static_methods=True,
        protected=False,
        private=False,
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

    def check(self, method: Method) -> bool:
        for check in self.checks:
            if check(method):
                return False
        return True

    def extract(self, methods: list[Method]) -> list[Method]:
        return [i for i in methods if self.check(i)]


__all__ = ["Method", "MethodFilter"]
