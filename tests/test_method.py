from objinspect import Class
from objinspect.method import Method, MethodFilter


class ClassTestA:
    def inherited_method(self):
        """Inherited method"""
        print("Called inherited")


class ClassTestB(ClassTestA):
    def __init__(self) -> None:
        """__init__ method"""
        print("init")

    def public_method(self, a: int, b: str = "b") -> None:
        """Public method"""
        print("Called public_method")

    def __private_method(self) -> None:
        """Private method"""
        print("Called __private_method")

    def _protected_method(self) -> None:
        """Protected method"""
        print("Called _protected_method")

    @staticmethod
    def static_method():
        """Static method"""
        print("Called static_method")

    @classmethod
    def class_method(cls):
        """Class method"""
        print("Called class_method")

    @property
    def property_method(self):
        """Property"""
        return "property"


def test_method():
    assert Method(ClassTestB.public_method, ClassTestB).is_public
    assert Method(ClassTestB._protected_method, ClassTestB).is_protected
    assert Method(ClassTestB.static_method, ClassTestB).is_static
    assert Method(ClassTestB.class_method, ClassTestB).is_classmethod


def test_method_inherited():
    assert Method(ClassTestB.inherited_method, ClassTestB).is_inherited
    assert not Method(ClassTestB.public_method, ClassTestB).is_inherited
    assert not Method(ClassTestB._protected_method, ClassTestB).is_inherited
    assert not Method(ClassTestB.static_method, ClassTestB).is_inherited
    assert not Method(ClassTestB.class_method, ClassTestB).is_inherited


def test_method_public():
    assert not Method(ClassTestB._protected_method, ClassTestB).is_public
    assert Method(ClassTestB.public_method, ClassTestB).is_public
    assert Method(ClassTestB.static_method, ClassTestB).is_public
    assert Method(ClassTestB.class_method, ClassTestB).is_public
    assert Method(ClassTestB.inherited_method, ClassTestB).is_public


def test_method_protected():
    assert Method(ClassTestB._protected_method, ClassTestB).is_protected
    assert not Method(ClassTestB.public_method, ClassTestB).is_protected
    assert not Method(ClassTestB.static_method, ClassTestB).is_protected
    assert not Method(ClassTestB.class_method, ClassTestB).is_protected
    assert not Method(ClassTestB.inherited_method, ClassTestB).is_protected


def test_method_static():
    assert Method(ClassTestB.static_method, ClassTestB).is_static
    assert not Method(ClassTestB.public_method, ClassTestB).is_static
    assert not Method(ClassTestB.class_method, ClassTestB).is_static
    assert not Method(ClassTestB.inherited_method, ClassTestB).is_static
    assert not Method(ClassTestB._protected_method, ClassTestB).is_static


def test_class_method():
    assert Method(ClassTestB.class_method, ClassTestB).is_classmethod
    assert not Method(ClassTestB.public_method, ClassTestB).is_classmethod
    assert not Method(ClassTestB.static_method, ClassTestB).is_classmethod
    assert not Method(ClassTestB.inherited_method, ClassTestB).is_classmethod
    assert not Method(ClassTestB._protected_method, ClassTestB).is_classmethod


def test_extractor():
    ALL_METHODS = Class(ClassTestB).methods
    assert "__init__" not in [i.name for i in MethodFilter(init=False).extract(ALL_METHODS)]
    assert "__private_method" not in [
        i.name for i in MethodFilter(private=False).extract(ALL_METHODS)
    ]
    assert "public_method" not in [i.name for i in MethodFilter(public=False).extract(ALL_METHODS)]
    assert "_protected_method" not in [
        i.name for i in MethodFilter(protected=False).extract(ALL_METHODS)
    ]
    assert "static_method" not in [
        i.name for i in MethodFilter(static_methods=False).extract(ALL_METHODS)
    ]
    assert "inherited_method" not in [
        i.name for i in MethodFilter(inherited=False).extract(ALL_METHODS)
    ]
