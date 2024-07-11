# objinspect
   
[![Tests](https://github.com/zigai/objinspect/actions/workflows/tests.yml/badge.svg)](https://github.com/zigai/objinspect/actions/workflows/tests.yml)
[![PyPI version](https://badge.fury.io/py/objinspect.svg)](https://badge.fury.io/py/objinspect)
![Supported versions](https://img.shields.io/badge/python-3.10+-blue.svg)
[![Downloads](https://static.pepy.tech/badge/objinspect)](https://pepy.tech/project/objinspect)
[![license](https://img.shields.io/github/license/zigai/objinspect.svg)](https://github.com/zigai/objinspect/blob/main/LICENSE)

objinspect is a high-level wrapper around Python's built-in `inspect` module. 
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
[
   {
      "default":"<class""inspect._empty"">",
      "description":"None",
      "kind":"<_ParameterKind.POSITIONAL_ONLY":0>,
      "name":"x",
      "type":"<class""inspect._empty"">"
   },
   {
      "default":"<class""inspect._empty"">",
      "description":"None",
      "kind":"<_ParameterKind.POSITIONAL_ONLY":0>,
      "name":"y",
      "type":"<class""inspect._empty"">"
   }
]
                 
>>> inspect(inspect)
Function(
    name="inspect",
    parameters=2,
    description="The inspect function  takes an object and an optional include_inherited flag (defaults to True) and returns either a Function object or a Class object depending on the type of object.",
)
```
### prettydir
![image](https://github.com/zigai/objinspect/assets/69588680/e1adcf90-0ef3-49e4-8804-a662f6388475)


## License
[MIT License](https://github.com/zigai/obj-inspect/blob/master/LICENSE)
