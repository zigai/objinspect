from examples import ExampleClassC

from objinspect import Class
from objinspect.method import Method, MethodFilter


def test_method():
    assert Method(ExampleClassC.public_method, ExampleClassC).is_public
    assert Method(ExampleClassC._protected_method, ExampleClassC).is_protected
    assert Method(ExampleClassC.static_method, ExampleClassC).is_static
    assert Method(ExampleClassC.class_method, ExampleClassC).is_classmethod


def test_method_inherited():
    assert Method(ExampleClassC.inherited_method, ExampleClassC).is_inherited
    assert not Method(ExampleClassC.public_method, ExampleClassC).is_inherited
    assert not Method(ExampleClassC._protected_method, ExampleClassC).is_inherited
    assert not Method(ExampleClassC.static_method, ExampleClassC).is_inherited
    assert not Method(ExampleClassC.class_method, ExampleClassC).is_inherited


def test_method_public():
    assert not Method(ExampleClassC._protected_method, ExampleClassC).is_public
    assert Method(ExampleClassC.public_method, ExampleClassC).is_public
    assert Method(ExampleClassC.static_method, ExampleClassC).is_public
    assert Method(ExampleClassC.class_method, ExampleClassC).is_public
    assert Method(ExampleClassC.inherited_method, ExampleClassC).is_public


def test_method_protected():
    assert Method(ExampleClassC._protected_method, ExampleClassC).is_protected
    assert not Method(ExampleClassC.public_method, ExampleClassC).is_protected
    assert not Method(ExampleClassC.static_method, ExampleClassC).is_protected
    assert not Method(ExampleClassC.class_method, ExampleClassC).is_protected
    assert not Method(ExampleClassC.inherited_method, ExampleClassC).is_protected


def test_method_static():
    assert Method(ExampleClassC.static_method, ExampleClassC).is_static
    assert not Method(ExampleClassC.public_method, ExampleClassC).is_static
    assert not Method(ExampleClassC.class_method, ExampleClassC).is_static
    assert not Method(ExampleClassC.inherited_method, ExampleClassC).is_static
    assert not Method(ExampleClassC._protected_method, ExampleClassC).is_static


def test_class_method():
    assert Method(ExampleClassC.class_method, ExampleClassC).is_classmethod
    assert not Method(ExampleClassC.public_method, ExampleClassC).is_classmethod
    assert not Method(ExampleClassC.static_method, ExampleClassC).is_classmethod
    assert not Method(ExampleClassC.inherited_method, ExampleClassC).is_classmethod
    assert not Method(ExampleClassC._protected_method, ExampleClassC).is_classmethod


def test_extractor():
    ALL_METHODS = Class(ExampleClassC).methods
    assert "__init__" not in [i.name for i in MethodFilter(init=False).extract(ALL_METHODS)]
    assert "public_method" not in [i.name for i in MethodFilter(public=False).extract(ALL_METHODS)]
    assert "__private_method" not in [
        i.name for i in MethodFilter(private=False).extract(ALL_METHODS)
    ]
    assert "_protected_method" not in [
        i.name for i in MethodFilter(protected=False).extract(ALL_METHODS)
    ]
    assert "static_method" not in [
        i.name for i in MethodFilter(static_methods=False).extract(ALL_METHODS)
    ]
    assert "inherited_method" not in [
        i.name for i in MethodFilter(inherited=False).extract(ALL_METHODS)
    ]
