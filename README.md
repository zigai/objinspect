# objinspect

View the structure of Python classes and functions.

# Installation
#### From PyPi
```
pip install objinspect
```
#### From source
```
pip install git+https://github.com/zigai/obj-inspect
```

# Examples
```python
>>> from objinspect import objinspect
>>> objinspect(objinspect)
>>> Function(name='objinspect', parameters=2, description='The objinspect function  takes an object and an optional include_inherited flag (defaults to True) and returns either a Function object or a Class object depending on the type of object.')
```
``` python
>>> import math
>>> from objinspect import objinspect
>>> objinspect(math.pow)
Function(name='pow', parameters=2, description='Return x**y (x to the power of y).')
```
``` python
>>> objinspect(math.pow).dict
{'name': 'pow', 'parameters': [{'name': 'x', 'kind': <_ParameterKind.POSITIONAL_ONLY: 0>, 'type': <class 'inspect._empty'>, 'default': <class 'inspect._empty'>, 'description': None}, {'name': 'y', 'kind': <_ParameterKind.POSITIONAL_ONLY: 0>, 'type': <class 'inspect._empty'>, 'default': <class 'inspect._empty'>, 'description': None}], 'docstring': 'Return x**y (x to the power of y).'}
```
# License
[MIT License](https://github.com/zigai/obj-inspect/blob/master/LICENSE)
