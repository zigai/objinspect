from objinspect import MethodExtractor


class ClassTestA:
    def inherited_method(self):
        """INHERITED METHOD"""
        print("Called inherited")


class ClassTestB(ClassTestA):
    def __init__(self) -> None:
        """__init__ method"""
        print("init")

    def public_method(self, a: int, b: str = "b") -> None:
        """PUBLIC METHOD"""
        print("Called public_method")

    def __private_method(self) -> None:
        """PRIVATE METHOD"""
        print("Called __private_method")

    def _protected_method(self) -> None:
        """PROTECTED METHOD"""
        print("Called _protected_method")

    @staticmethod
    def static_method():
        """STATIC METHOD"""
        print("Called static_method")

    @classmethod
    def class_method(cls):
        """CLASS METHOD"""
        print("Called class_method")

    @property
    def property_method(self):
        """PROPERTY METHOD"""
        return "property"


def test_extractor():
    assert "__init__" not in [i.name for i in MethodExtractor(init=False).extract(ClassTestB)]
    assert "__private_method" not in [
        i.name for i in MethodExtractor(private=False).extract(ClassTestB)
    ]
    assert "public_method" not in [
        i.name for i in MethodExtractor(public=False).extract(ClassTestB)
    ]
    assert "_protected_method" not in [
        i.name for i in MethodExtractor(protected=False).extract(ClassTestB)
    ]
    assert "static_method" not in [
        i.name for i in MethodExtractor(static_methods=False).extract(ClassTestB)
    ]
    assert "inherited_method" not in [
        i.name for i in MethodExtractor(inherited=False).extract(ClassTestB)
    ]
