from examples import ExampleClassA, example_function

from objinspect import Class, Function, Method, objinspect


def test_correct_return_types():
    assert isinstance(objinspect(ExampleClassA("a", 1).method_1), Method)
    assert isinstance(objinspect(example_function), Function)
    assert isinstance(objinspect(ExampleClassA), Class)


def test_method_of_instance():
    obj = objinspect(ExampleClassA("a", 1).method_1)
    assert isinstance(obj, Method)
    print(obj.cls)
