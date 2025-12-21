# objinspect

[![Tests](https://github.com/zigai/objinspect/actions/workflows/tests.yml/badge.svg)](https://github.com/zigai/objinspect/actions/workflows/tests.yml)
[![Documentation Status](https://readthedocs.org/projects/objinspect/badge/?version=latest)](https://objinspect.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/objinspect.svg)](https://badge.fury.io/py/objinspect)
![Supported versions](https://img.shields.io/badge/python-3.10+-blue.svg)
[![Downloads](https://static.pepy.tech/badge/objinspect)](https://pepy.tech/project/objinspect)
[![license](https://img.shields.io/github/license/zigai/objinspect.svg)](https://github.com/zigai/objinspect/blob/main/LICENSE)

`objinspect` is a high-level wrapper around Python's built-in `inspect` module.
It provides a simple interface for examining Python functions and classes.

## Features
- Simplified inspection of Python objects (classes, functions, methods)
- Detailed information about parameters, return types, and docstrings
- prettydir - like dir(), but with more information and prettier output

## Installation
#### From PyPi
```
pip install objinspect
```
#### From source
```
pip install git+https://github.com/zigai/objinspect
```

## Examples

``` python
>>> from objinspect import inspect, pdir
>>> import math
>>> inspect(math.pow)
Function(name='pow', parameters=2, description='Return x**y (x to the power of y).')

>>> inspect(math.pow).dict
{
   'name': 'pow',
   'parameters': [
      {'name': 'x', 'kind': <_ParameterKind.POSITIONAL_ONLY: 0>, 'type': <class 'inspect._empty'>, 'default': <class 'inspect._empty'>, 'description': None},
      {'name': 'y', 'kind': <_ParameterKind.POSITIONAL_ONLY: 0>, 'type': <class 'inspect._empty'>, 'default': <class 'inspect._empty'>, 'description': None}],
   'docstring': 'Return x**y (x to the power of y).'
}

>>> inspect(inspect)
Function(name='inspect', parameters=8, description='Inspects an object and returns a structured representation of its attributes and methods.')
```
### prettydir
![image](https://github.com/zigai/objinspect/assets/69588680/e1adcf90-0ef3-49e4-8804-a662f6388475)


## License
[MIT License](https://github.com/zigai/obj-inspect/blob/master/LICENSE)
