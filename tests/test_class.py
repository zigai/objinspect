import pytest
from interfacy_core.interfacy_class import InterfacyClass


class ExampleClass1:
    """ExampleClass1 dostring"""

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


cls1 = InterfacyClass(ExampleClass1)

# ---


def test_getitem():
    assert cls1["__init__"].name == "__init__"
    assert cls1[0].name == "__init__"
    assert cls1["method_1"].name == "method_1"
    with pytest.raises(IndexError):
        cls1[3]
    with pytest.raises(TypeError):
        cls1[3.3]
    with pytest.raises(KeyError):
        cls1["abc"]


def test_init():
    assert cls1.has_init == True


def test_description():
    assert cls1.description == "ExampleClass1 dostring"


def test_methods_len():
    assert len(cls1.methods) == 2


def test_init_first():
    assert cls1[0].name == "__init__"
