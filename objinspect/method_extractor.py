import inspect
from typing import Any, Callable

from objinspect.method import Method


class MethodExtractor:
    def __init__(
        self,
        init=True,
        public=True,
        inherited=True,
        static_methods=True,
        protected=False,
        private=False,
    ) -> None:
        self.name_filters = []
        self.method_filters = []
        self.cls = None

        if not init:
            self.name_filters.append(lambda name: name == "__init__")
        if not static_methods:
            self.name_filters.append(self._is_static_method)
        if not inherited:
            self.method_filters.append(lambda method: not self._is_inherited(method))
        if not private:
            self.name_filters.append(self._is_private_method)
        if not protected:
            self.name_filters.append(self._is_protected_method)
        if not public:
            self.name_filters.append(self._is_public_method)

    def _is_static_method(self, name: str) -> bool:
        return isinstance(inspect.getattr_static(self.cls, name), staticmethod)

    def _is_private_method(self, name: str) -> bool:
        return name.startswith(f"_{self.cls.__name__}__")

    def _is_protected_method(self, name: str) -> bool:
        return name.startswith("_") and not name.startswith("__")

    def _is_public_method(self, name: str) -> bool:
        return not name.startswith("_")

    def _is_inherited(self, method: Callable) -> bool:
        return method.__qualname__.startswith(self.cls.__name__)

    def check_method(self, name: str, method: Callable) -> bool:
        for f in self.name_filters:
            if f(name):
                return False
        for f in self.method_filters:
            if f(method):
                return False
        return True

    def extract(self, cls) -> list[Method]:
        self.cls = cls
        members = inspect.getmembers(cls, inspect.isfunction)
        return [Method(i[1]) for i in members if self.check_method(*i)]


__all__ = ["MethodExtractor"]
