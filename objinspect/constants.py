import inspect

inspect._empty.__repr__ = lambda: "EMPTY"
inspect._empty.__str__ = lambda: "EMPTY"
EMPTY = inspect._empty

__all__ = ["EMPTY"]
