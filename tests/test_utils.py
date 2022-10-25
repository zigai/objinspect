from py_inspect import util


def test_type_as_str():
    assert util.type_to_str(util.UnionParameter) == "UnionParameter"
