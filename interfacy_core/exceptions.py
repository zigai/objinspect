from interfacy_core.util import type_as_str


class InterfacyException(Exception):
    pass


class UnsupportedParamError(InterfacyException):
    def __init__(self, t):
        self.msg = f"Parameter of type '{type_as_str(t)}' is not supported"
        super().__init__(self.msg)
