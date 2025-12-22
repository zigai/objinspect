import pytest
from examples import ExampleClassA, ExampleClassC

from objinspect import Class

obj = Class(ExampleClassA)


def test_getitem():
    assert obj.get_method("__init__").name == "__init__"
    assert obj.has_init == True
    assert obj.get_method(0).name == "__init__"
    assert obj.get_method("method_1").name == "method_1"
    assert len(obj.methods) == 3
    with pytest.raises(IndexError):
        obj.get_method(3)
    with pytest.raises(TypeError):
        obj.get_method(3.3)
    with pytest.raises(KeyError):
        obj.get_method("abc")


def test_init():
    assert obj.has_init == True


def test_description():
    assert obj.description == "ExampleClassA dostring"


def test_methods_len():
    assert len(obj.methods) == 3


def test_init_2():
    with pytest.raises(ValueError):
        obj.call_method("method_2")

    obj.init("a", 1)
    assert obj.instance.a == "a"
    assert obj.instance.b == 1
    assert obj.call_method("method_2") == "a1"


def test_instance():
    iobj = Class(ExampleClassA("a", 1))
    assert iobj.instance is not None
    assert iobj.is_initialized

    assert iobj.instance.a == "a"
    assert iobj.instance.b == 1
    assert len(iobj.methods) == 3
    assert iobj.call_method("method_2") == "a1"


def test_class_instance_initialization():
    instance = ExampleClassA("test", 123)
    cls = Class(instance)
    assert cls.is_initialized
    assert cls.instance == instance
    assert cls.name == "ExampleClassA instance"


def test_class_inheritance():
    cls = Class(ExampleClassC)
    inherited_methods = [method for method in cls.methods if method.is_inherited]
    assert any(method.name == "inherited_method" for method in inherited_methods)


def test_class_includes_classmethods_when_enabled():
    cls = Class(ExampleClassC, classmethod=True)
    assert "class_method" in [method.name for method in cls.methods]


def test_instance_classmethod_filter_only_excludes_classmethods():
    instance = ExampleClassC()
    cls = Class(instance, classmethod=False)
    method_names = [method.name for method in cls.methods]
    assert "public_method" in method_names
    assert "class_method" not in method_names
