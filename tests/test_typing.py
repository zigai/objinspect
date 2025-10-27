import typing
from collections import OrderedDict, defaultdict
from enum import Enum, Flag, auto
from typing import Any, DefaultDict, Dict, List, Optional, Set, Tuple, Union

import pytest
from typing_extensions import Literal

from objinspect.typing import (
    get_enum_choices,
    get_literal_choices,
    is_direct_literal,
    is_enum,
    is_generic_alias,
    is_iterable_type,
    is_mapping_type,
    is_or_contains_literal,
    is_union_type,
    literal_contains,
    type_name,
    type_simplified,
)


class TestIsDirectLiteral:
    def test_literal_type_check(self):
        assert is_direct_literal(typing.Literal["a", "b"])

    def test_nested_literal_type_check(self):
        assert not is_direct_literal(typing.Union[typing.Literal["a"], typing.Literal["b"]])

    def test_literal_or_none(self):
        assert not is_direct_literal(typing.Literal["b"] | None)

    def test_basic_type_as_literal(self):
        assert not is_direct_literal(str)

    def test_literal_as_literal(self):
        assert not is_direct_literal(typing.Literal)


class TestIsLiteral:
    def test_literal_type(self):
        assert is_or_contains_literal(typing.Literal["a", "b"])

    def test_non_literal_type(self):
        assert not is_or_contains_literal(int)

    def test_nested_literal_type(self):
        nested_literal = typing.Literal[typing.Literal["a", "b"]]
        assert is_or_contains_literal(nested_literal)

    def test_literal_or_none(self):
        literal_or_none = typing.Literal["a", "b"] | None
        assert is_or_contains_literal(literal_or_none)

    def test_composite_without_literal(self):
        composite_without_literal = typing.Union[int, str]
        assert not is_or_contains_literal(composite_without_literal)


class TestLiteralContains:
    def test_value_matches_literal(self):
        assert literal_contains(typing.Literal["a", "b", "c"], "a")

    def test_value_does_not_match_literal(self):
        assert not literal_contains(typing.Literal["a", "b", "c"], "d")

    def test_invalid_literal_type(self):
        with pytest.raises(ValueError):
            literal_contains(int, 1)

    def test_none_value(self):
        assert not literal_contains(typing.Literal["a", "b", "c"], None)

    def test_complex_value(self):
        class CustomClass:
            pass

        assert not literal_contains(typing.Literal["a", "b", "c"], CustomClass())

    def test_empty_literal(self):
        with pytest.raises(ValueError):
            literal_contains(typing.Literal[()], "a")


class TestGetLiteralChoices:
    def test_get_choices_from_literal(self):
        assert get_literal_choices(typing.Literal["a", "b"]) == ("a", "b")

    def test_invalid_literal_type_for_choices(self):
        with pytest.raises(ValueError):
            get_literal_choices(int)

    def test_empty_literal_for_choices(self):
        with pytest.raises(ValueError):
            get_literal_choices(typing.Literal)


class TestIsIterableType:
    def test_is_iterable_type_simple(self):
        assert not is_iterable_type(int)
        assert is_iterable_type(list)
        assert is_iterable_type(str)
        assert is_iterable_type(dict)
        assert is_iterable_type(set)
        assert is_iterable_type(tuple)

    def test_is_iterable_type_alias(self):
        assert is_iterable_type(list[int])
        assert is_iterable_type(list[int | float])
        assert is_iterable_type(tuple[int])

    def test_is_iterable_type_typing(self):
        assert is_iterable_type(typing.List)
        assert is_iterable_type(typing.Dict)
        assert is_iterable_type(typing.Sequence)
        assert is_iterable_type(typing.Set)
        assert is_iterable_type(typing.Deque)


class TestIsMappingType:
    def test_is_mapping_type_typing(self):
        assert is_mapping_type(OrderedDict)
        assert is_mapping_type(defaultdict)
        assert is_mapping_type(typing.Dict)
        assert is_mapping_type(typing.Mapping)
        assert is_mapping_type(typing.OrderedDict)
        assert is_mapping_type(typing.DefaultDict)

    def test_is_mapping_type_simple(self):
        assert not is_mapping_type(int)
        assert not is_mapping_type(list)
        assert not is_mapping_type(str)
        assert is_mapping_type(dict)

    def test_is_mapping_type_alias(self):
        assert is_mapping_type(dict[str, int])
        assert is_mapping_type(dict[str, int | float])


class TestIsGenericAlias:
    @pytest.fixture
    def generic_types(self):
        return [
            List[int],
            Dict[str, int],
            Tuple[str, int],
            Set[float],
            List[Dict[str, Set[int]]],
            defaultdict[str, int],
            DefaultDict[str, int],
            OrderedDict[str, int],
        ]

    def test_positive_cases(self, generic_types):
        for type_hint in generic_types:
            print(type(List[int]))
            print(type(List))
            assert is_generic_alias(type_hint)

    def test_negative_cases(self):
        non_generic_types = [int, str, List, Dict, Union[int, str], Any]
        for type_hint in non_generic_types:
            print(type(List[int]))
            print(type(List))
            assert not is_generic_alias(type_hint)

    def test_custom_generic(self):
        from typing import Generic, TypeVar

        T = TypeVar("T")

        class MyGeneric(Generic[T]):
            pass

        assert is_generic_alias(MyGeneric[int])
        assert not is_generic_alias(MyGeneric)

    def test_edge_cases(self):
        assert not is_generic_alias(None)
        assert not is_generic_alias(...)  # Ellipsis
        assert not is_generic_alias(type(None))


class TestIsUnionType:
    @pytest.fixture
    def union_types(self):
        return {
            "simple_union": Union[int, str],
            "multi_union": Union[int, str, float],
            "optional": Optional[int],
            "nested_union": Union[int, Union[str, float]],
        }

    def test_positive_cases(self, union_types):
        for type_hint in union_types.values():
            assert is_union_type(type_hint)

    def test_negative_cases(self):
        non_union_types = [int, str, List[int], Dict[str, int], Any]
        for type_hint in non_union_types:
            assert not is_union_type(type_hint)

    def test_new_union_syntax(self):
        assert is_union_type(int | str)
        assert is_union_type(int | str | float)
        assert not is_union_type(int | int)  # same as just int

    def test_edge_cases(self):
        assert not is_union_type(None)
        assert not is_union_type(...)
        assert not is_union_type(Union)  # Union itself, not a union type

    def test_nested_unions(self):
        NestedUnion = Union[int, Union[str, float]]
        assert is_union_type(NestedUnion)
        assert is_union_type(Union[NestedUnion, bool])

    @pytest.mark.parametrize(
        "type_hint,expected",
        [
            (Union[int, str], True),
            (Optional[int], True),
            (List[int], False),
            (int, False),
            (Any, False),
        ],
    )
    def test_parametrized(self, type_hint, expected):
        assert is_union_type(type_hint) == expected


class TestTypeName:
    @pytest.mark.parametrize(
        "input_type,expected",
        [
            (int, "int"),
            (str, "str"),
            (Any, "Any"),
            (typing.Any, "Any"),
            (Union[int, str], "int | str"),
            (typing.Union[int, str], "int | str"),
            (List[int], "List[int]"),
            (typing.List[int], "List[int]"),
        ],
    )
    def test_type_name(self, input_type, expected):
        assert type_name(input_type) == expected

    def test_custom_class(self):
        class CustomClass:
            pass

        assert type_name(CustomClass) == "CustomClass"


class TestTypeSimplified:
    @pytest.mark.parametrize(
        "input_type,expected",
        [
            (int, int),
            (str, str),
            (List[int], list),
            (Dict[str, int], dict),
            (Union[int, str], (int, str)),
            (Optional[int], (int, type(None))),
            (Any, Any),
            (List[Dict[str, int]], list),
            (Tuple[int, str], tuple),
            (OrderedDict[str, int], OrderedDict),
            (defaultdict[str, int], defaultdict),
        ],
    )
    def test_type_simplified(self, input_type, expected):
        assert type_simplified(input_type) == expected

    def test_nested_types(self):
        assert type_simplified(List[Dict[str, List[int]]]) == list

    def test_custom_generic(self):
        from typing import Generic, TypeVar

        T = TypeVar("T")

        class MyGeneric(Generic[T]):
            pass

        assert type_simplified(MyGeneric[int]) == MyGeneric

    def test_complex_union(self):
        complex_type = Union[int, str, List[Dict[str, Any]]]
        simplified = type_simplified(complex_type)
        assert isinstance(simplified, tuple)
        assert set(simplified) == {int, str, list}

    def test_none_type(self):
        assert type_simplified(type(None)) == type(None)

    @pytest.mark.parametrize("var", [None, 42, "string", [1, 2, 3]])
    def test_non_type_inputs(self, var):
        assert type_simplified(var) == var


@pytest.fixture
def literal_types():
    return {
        "simple": Literal[1, 2, 3],
        "str_literal": Literal["a", "b", "c"],
        "mixed": Literal[1, "a", True],
        "nested": Union[int, Literal[1, 2]],
        "optional": Optional[Literal["x", "y"]],
    }


def test_is_direct_literal(literal_types):
    assert is_direct_literal(literal_types["simple"])
    assert is_direct_literal(literal_types["str_literal"])
    assert is_direct_literal(literal_types["mixed"])
    assert not is_direct_literal(Literal)
    assert not is_direct_literal(int)
    assert not is_direct_literal(literal_types["nested"])
    assert not is_direct_literal(literal_types["optional"])


def test_is_or_contains_literal(literal_types):
    assert is_or_contains_literal(literal_types["simple"])
    assert is_or_contains_literal(literal_types["str_literal"])
    assert is_or_contains_literal(literal_types["mixed"])
    assert is_or_contains_literal(literal_types["nested"])
    assert is_or_contains_literal(literal_types["optional"])
    assert not is_or_contains_literal(int)
    assert not is_or_contains_literal(Union[int, str])


@pytest.mark.parametrize(
    "literal_type, expected",
    [
        (Literal[1, 2, 3], (1, 2, 3)),
        (Literal["a", "b"], ("a", "b")),
        (Literal[True, False], (True, False)),
        (Union[int, Literal["x", "y"]], ("x", "y")),
        (Optional[Literal[1, 2]], (1, 2)),
    ],
)
def test_get_literal_choices(literal_type, expected):
    assert get_literal_choices(literal_type) == expected


def test_get_literal_choices_error():
    with pytest.raises(ValueError):
        get_literal_choices(int)


@pytest.mark.parametrize(
    "literal_type, value, expected",
    [
        (Literal[1, 2, 3], 2, True),
        (Literal[1, 2, 3], 4, False),
        (Literal["a", "b"], "a", True),
        (Literal["a", "b"], "c", False),
        (Literal[True, False], True, True),
        (Literal[True, False], None, False),
    ],
)
def test_literal_contains(literal_type, value, expected):
    assert literal_contains(literal_type, value) == expected


def test_literal_contains_error():
    with pytest.raises(ValueError):
        literal_contains(int, 1)


def test_nested_literal_structures():
    nested_literal = Union[Literal[1, 2], Literal["a", "b"]]
    assert is_or_contains_literal(nested_literal)
    assert not is_direct_literal(nested_literal)
    assert get_literal_choices(nested_literal) in {(1, 2), ("a", "b")}


def test_complex_union_with_literal():
    complex_union = Union[int, str, Literal[1, "a"], Optional[Literal[True, False]]]
    assert is_or_contains_literal(complex_union)
    assert not is_direct_literal(complex_union)
    assert get_literal_choices(complex_union) == (1, "a")


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class ColorString(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class Permissions(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()


class EmptyEnum(Enum):
    pass


@pytest.fixture
def enum_types():
    return {
        "color": Color,
        "color_string": ColorString,
        "permissions": Permissions,
        "empty": EmptyEnum,
    }


def test_is_enum(enum_types):
    assert is_enum(enum_types["color"])
    assert is_enum(enum_types["color_string"])
    assert is_enum(enum_types["permissions"])
    assert is_enum(enum_types["empty"])
    assert not is_enum(int)
    assert not is_enum(str)
    assert not is_enum(1)
    assert not is_enum("test")
    assert not is_enum(None)
    assert not is_enum(object())


def test_get_enum_choices(enum_types):
    assert get_enum_choices(enum_types["color"]) == ("RED", "GREEN", "BLUE")
    assert get_enum_choices(enum_types["color_string"]) == ("RED", "GREEN", "BLUE")
    assert get_enum_choices(enum_types["permissions"]) == ("READ", "WRITE", "EXECUTE")
    assert get_enum_choices(enum_types["empty"]) == ()


def test_get_enum_choices_error():
    with pytest.raises(TypeError):
        get_enum_choices(int)

    with pytest.raises(TypeError):
        get_enum_choices("")


@pytest.mark.parametrize(
    "enum_type,expected_len",
    [
        (Color, 3),
        (ColorString, 3),
        (Permissions, 3),
        (EmptyEnum, 0),
    ],
)
def test_get_enum_choices_length(enum_type, expected_len):
    assert len(get_enum_choices(enum_type)) == expected_len


def test_is_enum_with_custom_objects():
    class CustomClass:
        pass

    custom_obj = CustomClass()
    assert not is_enum(CustomClass)
    assert not is_enum(custom_obj)

    with pytest.raises(TypeError):
        get_enum_choices(custom_obj)
