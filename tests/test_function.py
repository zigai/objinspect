import asyncio

import pytest
from examples import async_example_function, example_function

from objinspect.constants import EMPTY
from objinspect.function import Function

func = Function(example_function)


def test_params_len():
    assert len(func._parameters) == 3


def test_getitem():
    assert func.get_param(0).name == "a"
    assert func.get_param(1).name == "b"
    assert func.get_param(2).name == "c"
    assert func.get_param("a").name == "a"
    assert func.get_param("b").name == "b"
    assert func.get_param("c").name == "c"
    assert func.return_type is int
    with pytest.raises(IndexError):
        func.get_param(3)
    with pytest.raises(TypeError):
        func.get_param(3.3)
    with pytest.raises(KeyError):
        func.get_param("d")


def test_type_inference():
    assert func.get_param("a").type is EMPTY
    assert func.get_param("b").type is type(None)
    assert func.get_param("c").type is int


def test_descriptions():
    assert func.has_docstring
    assert func.description == "example_function dostring"
    assert func.get_param("a").description == "Argument a"
    assert func.get_param("b").description == "Argument b. Defaults to None."
    assert func.get_param("c").description == "Argument c. Defaults to 4."


def test_is_param_typed():
    assert not func.get_param("a").is_typed
    assert func.get_param("b").is_typed
    assert func.get_param("c").is_typed


def test_is_param_optional():
    assert not func.get_param("a").is_optional
    assert func.get_param("b").is_optional
    assert func.get_param("c").is_optional


def test_call():
    from math import pow as math_pow

    assert Function(math_pow).call(2, 2) == 4


def test_async():
    async_func = Function(async_example_function)

    assert not func.is_coroutine
    assert async_func.is_coroutine


def test_call_async_with_sync_function():
    from math import pow as math_pow

    assert asyncio.run(Function(math_pow).call_async(2, 2)) == 4


def test_call_async_with_async_function():
    assert asyncio.run(Function(async_example_function).call_async(3)) == 4
