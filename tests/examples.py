class ExampleClassA:
    """ExampleClassA dostring"""

    def __init__(self, a: str, b: int) -> None:
        """__init__ method

        Args:
            a (str)
            b (int)
        """
        self.a = a
        self.b = b
        print("ExampleClassA init")

    def method_1(self):
        """Test docstring"""
        print("method test called")
        print(f"{self.a=}")
        print(f"{self.b=}")

    def method_2(self):
        return self.a + str(self.b)


class ExampleClassB:
    def inherited_method(self):
        """Inherited method"""
        print("Called inherited")


class ExampleClassC(ExampleClassB):
    def __init__(self) -> None:
        """__init__ method"""
        print("ExampleClassC init")

    def public_method(self, a: int, b: str = "b") -> None:
        """Public method"""
        print("Called public_method")

    def __private_method(self) -> None:
        """Private method"""
        print("Called __private_method")

    def _protected_method(self) -> None:
        """Protected method"""
        print("Called _protected_method")

    @staticmethod
    def static_method():
        """Static method"""
        print("Called static_method")

    @classmethod
    def class_method(cls):
        """Class method"""
        print("Called class_method")

    @property
    def property_method(self):
        """Property"""
        return "property"


class ExampleAsyncClass:
    def __init__(self, prefix: str = "value") -> None:
        self.prefix = prefix

    async def async_instance_method(self, value: int) -> str:
        return f"{self.prefix}:{value}"

    @staticmethod
    async def async_static_method(value: int) -> int:
        return value + 1

    @classmethod
    async def async_class_method(cls, value: str = "x") -> str:
        return f"{cls.__name__}:{value}"

    def sync_method(self, value: int) -> int:
        return value * 2


def example_function(a, b=None, c=4) -> int:
    """
    example_function dostring

    Args:
        a: Argument a
        b (optional): Argument b. Defaults to None.
        c (int, optional): Argument c. Defaults to 4.
    """
    return c * 2


async def async_example_function(value: int = 1) -> int:
    return value + 1
