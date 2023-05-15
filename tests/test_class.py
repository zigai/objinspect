import pytest

from objinspect import Class


class ExampleClassA:
    """ExampleClassA dostring"""

    def __init__(self, a: str, b: int) -> None:
        """__init__ method

        Args:
            a (str)
            b (int)
        """
        self.a = a
        self.b = b
        print("init")

    def method_1(self):
        """test docstring"""
        print("method test called")
        print(f"{self.a=}")
        print(f"{self.b=}")

    def method_2(self):
        return self.a + str(self.b)


A = Class(ExampleClassA)


def test_getitem():
    assert A.get_method("__init__").name == "__init__"
    assert A.has_init == True
    assert A.get_method(0).name == "__init__"
    assert A.get_method("method_1").name == "method_1"
    with pytest.raises(IndexError):
        A.get_method(3)
    with pytest.raises(TypeError):
        A.get_method(3.3)
    with pytest.raises(KeyError):
        A.get_method("abc")


def test_init():
    assert A.has_init == True


def test_description():
    assert A.description == "ExampleClass1 dostring"


def test_methods_len():
    assert len(A.methods) == 3


def test_init():
    with pytest.raises(ValueError):
        A.call_method("method_2")

    A.init("a", 1)
    assert A.instance.a == "a"
    assert A.instance.b == 1

    assert A.call_method("method_2") == "a1"
