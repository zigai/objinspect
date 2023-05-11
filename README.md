# objinspect
[![Tests](https://github.com/zigai/obj-inspect/actions/workflows/tests.yml/badge.svg)](https://github.com/zigai/obj-inspect/actions/workflows/tests.yml)
[![PyPI version](https://badge.fury.io/py/objinspect.svg)](https://badge.fury.io/py/objinspect)
![Supported versions](https://img.shields.io/badge/python-3.10+-blue.svg)
[![Downloads](https://static.pepy.tech/badge/objinspect)](https://pepy.tech/project/objinspect)
[![license](https://img.shields.io/github/license/zigai/objinspect.svg)](https://github.com/zigai/objinspect/blob/main/LICENSE)

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

# Example

``` python
>>> import math
>>> from objinspect import objinspect
>>> objinspect(math.pow)
Function(name='pow', parameters=2, description='Return x**y (x to the power of y).')

>>> objinspect(math.pow).dict
{'docstring': 'Return x**y (x to the power of y).',
 'name': 'pow',
 'parameters': [{'default': <class 'inspect._empty'>,
                 'description': None,
                 'kind': <_ParameterKind.POSITIONAL_ONLY: 0>,
                 'name': 'x',
                 'type': <class 'inspect._empty'>},
                {'default': <class 'inspect._empty'>,
                 'description': None,
                 'kind': <_ParameterKind.POSITIONAL_ONLY: 0>,
                 'name': 'y',
                 'type': <class 'inspect._empty'>}]                 
}
                 
>>> objinspect(objinspect)
>>> Function(name='objinspect', parameters=2, description='The objinspect function  takes an object and an optional include_inherited flag (defaults to True) and returns either a Function object or a Class object depending on the type of object.')
```
# License
[MIT License](https://github.com/zigai/obj-inspect/blob/master/LICENSE)
