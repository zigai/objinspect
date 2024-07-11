from examples import ExampleClassA, example_function

from objinspect import Class, Function, Method, inspect


def test_correct_return_types():
    assert isinstance(inspect(ExampleClassA("a", 1).method_1), Method)
    assert isinstance(inspect(example_function), Function)
    assert isinstance(inspect(ExampleClassA), Class)
    assert isinstance(inspect(lambda x: x), Function)


def test_method_of_instance():
    obj = inspect(ExampleClassA("a", 1).method_1)
    assert isinstance(obj, Method)
