from examples import (
    ExampleAsyncClass,
    ExampleClassA,
    ExampleClassC,
    async_example_function,
    example_function,
)

from objinspect import Class, Function, Method, inspect


def test_correct_return_types():
    assert isinstance(inspect(ExampleClassA("a", 1).method_1), Method)
    assert isinstance(inspect(example_function), Function)
    assert isinstance(inspect(async_example_function), Function)
    assert isinstance(inspect(ExampleAsyncClass.async_instance_method), Method)
    assert isinstance(inspect(ExampleClassA), Class)
    assert isinstance(inspect(lambda x: x), Function)


def test_method_of_instance():
    obj = inspect(ExampleClassA("a", 1).method_1)
    assert isinstance(obj, Method)


def test_inspect_classmethod_flag():
    default_obj = inspect(ExampleClassC)
    assert "class_method" not in [method.name for method in default_obj.methods]

    enabled_obj = inspect(ExampleClassC, classmethod=True)
    assert "class_method" in [method.name for method in enabled_obj.methods]


def test_inspect_async_metadata():
    assert inspect(async_example_function).is_coroutine
    assert inspect(ExampleAsyncClass.async_static_method).is_coroutine
    assert inspect(ExampleAsyncClass.async_class_method).is_coroutine
