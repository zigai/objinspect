from objinspect import Class
from objinspect.method import Method, MethodFilter


class ClassTestA:
    def inherited_method(self):
        """INHERITED METHOD"""
        print("Called inherited")


class ClassTestB(ClassTestA):
    def __init__(self) -> None:
        """__init__ method"""
        print("init")

    def public_method(self, a: int, b: str = "b") -> None:
        """PUBLIC METHOD"""
        print("Called public_method")

    def __private_method(self) -> None:
        """PRIVATE METHOD"""
        print("Called __private_method")

    def _protected_method(self) -> None:
        """PROTECTED METHOD"""
        print("Called _protected_method")

    @staticmethod
    def static_method():
        """STATIC METHOD"""
        print("Called static_method")

    @classmethod
    def class_method(cls):
        """CLASS METHOD"""
        print("Called class_method")

    @property
    def property_method(self):
        """PROPERTY METHOD"""
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

    all_methods = Class(ClassTestB).methods
    assert "__init__" not in [i.name for i in MethodFilter(init=False).extract(all_methods)]
    assert "__private_method" not in [
        i.name for i in MethodFilter(private=False).extract(all_methods)
    ]
    assert "public_method" not in [i.name for i in MethodFilter(public=False).extract(all_methods)]
    assert "_protected_method" not in [
        i.name for i in MethodFilter(protected=False).extract(all_methods)
    ]
    assert "static_method" not in [
        i.name for i in MethodFilter(static_methods=False).extract(all_methods)
    ]
    assert "inherited_method" not in [
        i.name for i in MethodFilter(inherited=False).extract(all_methods)
    ]
