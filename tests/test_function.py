import pytest
from interfacy_core.constants import EMPTY
from interfacy_core.interfacy_func import InterfacyFunction


def example_func1(a, b=None, c=4):
    """Test function 1

    Args:
        a: Argument a
        b (optional): Argument b. Defaults to None.
        c (int, optional): Argument c. Defaults to 4.
    """
    ...


function1 = InterfacyFunction(example_func1)

# ---------------


def test_params_len():
    assert len(function1.parameters) == 3


def test_getitem():
    assert function1[0].name == "a"
    assert function1[1].name == "b"
    assert function1[2].name == "c"
    assert function1["a"].name == "a"
    assert function1["b"].name == "b"
    assert function1["c"].name == "c"
    with pytest.raises(IndexError):
        function1[3]
    with pytest.raises(TypeError):
        function1[3.3]
    with pytest.raises(KeyError):
        function1["d"]


def test_type_inference():
    assert function1["a"].type is EMPTY
    assert function1["b"].type is EMPTY
    assert function1["c"].type is int


def test_descriptions():
    assert function1.has_docstring == True
    assert function1.description == "Test function 1"
    assert function1["a"].description == "Argument a"
    assert function1["b"].description == "Argument b. Defaults to None."
    assert function1["c"].description == "Argument c. Defaults to 4."


def test_is_param_typed():
    assert function1["a"].is_typed == False
    assert function1["b"].is_typed == False
    assert function1["c"].is_typed == True


def test_is_param_optional():
    assert function1["a"].is_optional == False
    assert function1["b"].is_optional == True
    assert function1["c"].is_optional == True
