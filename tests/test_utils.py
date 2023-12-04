import typing as T

import pytest

from objinspect.util import (
    create_function,
    get_literal_choices,
    is_literal,
    is_pure_literal,
    literal_contains,
)


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


class TestIsPureLiteral:
    def test_literal_type_check(self):
        assert is_pure_literal(T.Literal["a", "b"])

    def test_nested_literal_type_check(self):
        assert not is_pure_literal(T.Union[T.Literal["a"], T.Literal["b"]])

    def test_literal_or_none(self):
        assert not is_pure_literal(T.Literal["b"] | None)

    def test_basic_type_as_literal(self):
        assert not is_pure_literal(str)

    def test_t_literal_as_literal(self):
        assert not is_pure_literal(T.Literal)


class TestIsLiteral:
    def test_literal_type(self):
        assert is_literal(T.Literal["a", "b"])

    def test_non_literal_type(self):
        assert not is_literal(int)

    def test_nested_literal_type(self):
        nested_literal = T.Literal[T.Literal["a", "b"]]
        assert is_literal(nested_literal)

    def test_literal_or_none(self):
        literal_or_none = T.Literal["a", "b"] | None
        assert is_literal(literal_or_none)

    def test_composite_without_literal(self):
        composite_without_literal = T.Union[int, str]
        assert not is_literal(composite_without_literal)


class TestIsInLiteral:
    def test_value_matches_literal(self):
        assert literal_contains(T.Literal["a", "b", "c"], "a")

    def test_value_does_not_match_literal(self):
        assert not literal_contains(T.Literal["a", "b", "c"], "d")

    def test_invalid_literal_type(self):
        with pytest.raises(ValueError):
            literal_contains(int, 1)

    def test_none_value(self):
        assert not literal_contains(T.Literal["a", "b", "c"], None)

    def test_complex_value(self):
        class CustomClass:
            pass

        assert not literal_contains(T.Literal["a", "b", "c"], CustomClass())

    def test_empty_literal(self):
        with pytest.raises(ValueError):
            literal_contains(T.Literal[()], "a")


class TestGetLiteralChoices:
    def test_get_choices_from_literal(self):
        assert get_literal_choices(T.Literal["a", "b"]) == ("a", "b")

    def test_invalid_literal_type_for_choices(self):
        with pytest.raises(ValueError):
            get_literal_choices(int)

    def test_empty_literal_for_choices(self):
        with pytest.raises(ValueError):
            get_literal_choices(T.Literal)
