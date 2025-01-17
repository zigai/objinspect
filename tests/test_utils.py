import pytest

from objinspect.util import create_function


class TestCreateFunction:
    def test_function_creation_with_valid_input(self):
        def mock_function(a, b):
            return a + b

        add = create_function(
            name="add",
            args={"a": (int, None), "b": (int, None)},
            body="return a + b",
            globs=globals(),
        )
        assert add(1, 2) == mock_function(1, 2)

    def test_function_with_defaults(self):
        add = create_function(
            name="add", args={"a": (int, 1), "b": (int, 2)}, body="return a + b", globs=globals()
        )
        assert add() == 3
        assert add(2) == 4
        assert add(b=3) == 4

    def test_globals_setup(self):
        globals_dict = {"external_var": 10}
        use_globals = create_function(
            name="use_globals", args={}, body="return external_var", globs=globals_dict
        )
        assert use_globals() == 10

    def test_return_type_handling(self):
        str_func = create_function(
            name="return_str", args={}, body='return "test"', globs=globals(), return_type=str
        )
        assert isinstance(str_func(), str)

    def test_docstring_assignment(self):
        func_with_docstring = create_function(
            name="func_with_docstring",
            args={},
            body="pass",
            globs=globals(),
            docstring="This is a test function.",
        )
        assert func_with_docstring.__doc__ == "This is a test function."

    def test_error_on_invalid_input(self):
        with pytest.raises(SyntaxError):
            create_function(name="1_invalid", args={}, body="pass", globs=globals())

    def test_body_execution(self):
        increment = create_function(
            name="increment", args={"x": (int,)}, body="return x + 1", globs=globals()
        )
        assert increment(1) == 2

    def test_edge_cases(self):
        nop = create_function(name="nop", args={}, body="pass", globs=globals())
        assert nop() is None
