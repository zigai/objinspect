from interfacy_core import util


def test_type_as_str():
    assert util.type_as_str(util.UnionTypeParameter) == "UnionTypeParameter"
