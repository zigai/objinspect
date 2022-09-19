from docstring_parser import Docstring


def has_docstring(docstring: str | None) -> bool:
    if docstring is None:
        return False
    return len(docstring) != 0


def docstring_description(docstring: Docstring | None) -> str:
    if docstring is None:
        return ""
    if docstring.short_description:
        return docstring.short_description
    if docstring.long_description:
        return docstring.long_description
    return ""


class UnionTypeParameter:
    def __init__(self, params: tuple) -> None:
        self.params = params


def type_as_str(t):
    type_str = repr(t)
    if "<class '" in type_str:
        type_str = type_str.split("'")[1]
    return type_str.split(".")[-1]
