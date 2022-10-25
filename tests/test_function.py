import pytest
from py_inspect.constants import EMPTY
from py_inspect.function import Function


def example_func1(a, b=None, c=4):
    """Test function 1

    Args:
        a: Argument a
        b (optional): Argument b. Defaults to None.
        c (int, optional): Argument c. Defaults to 4.
    """
    ...


function1 = Function(example_func1)


def test_params_len():
    assert len(function1._parameters) == 3


def test_getitem():
    assert function1.get_param(0).name == "a"
    assert function1.get_param(1).name == "b"
    assert function1.get_param(2).name == "c"
    assert function1.get_param("a").name == "a"
    assert function1.get_param("b").name == "b"
    assert function1.get_param("c").name == "c"
    with pytest.raises(IndexError):
        function1.get_param(3)
    with pytest.raises(TypeError):
        function1.get_param(3.3)
    with pytest.raises(KeyError):
        function1.get_param("d")


def test_type_inference():
    assert function1.get_param("a").type is EMPTY
    assert function1.get_param("b").type is EMPTY
    assert function1.get_param("c").type is int


def test_descriptions():
    assert function1.has_docstring == True
    assert function1.description == "Test function 1"
    assert function1.get_param("a").description == "Argument a"
    assert function1.get_param("b").description == "Argument b. Defaults to None."
    assert function1.get_param("c").description == "Argument c. Defaults to 4."


def test_is_param_typed():
    assert function1.get_param("a").is_typed == False
    assert function1.get_param("b").is_typed == False
    assert function1.get_param("c").is_typed == True


def test_is_param_optional():
    assert function1.get_param("a").is_optional == False
    assert function1.get_param("b").is_optional == True
    assert function1.get_param("c").is_optional == True
