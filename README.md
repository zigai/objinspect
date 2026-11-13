# objinspect

[![tests](https://img.shields.io/github/actions/workflow/status/zigai/objinspect/tests.yml?branch=master&label=tests&labelColor=30363d)](https://github.com/zigai/objinspect/actions/workflows/tests.yml)
[![docs](https://img.shields.io/readthedocs/objinspect?label=docs&logo=readthedocs&logoColor=white&labelColor=30363d)](https://objinspect.readthedocs.io/en/latest/)
[![PyPI](https://img.shields.io/pypi/v/objinspect?label=PyPI&color=blue&logo=pypi&logoColor=white&labelColor=30363d)](https://pypi.org/project/objinspect/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white&labelColor=30363d)](pyproject.toml)
[![downloads](https://img.shields.io/pypi/dm/objinspect?label=downloads&color=blue&labelColor=30363d)](https://pepy.tech/projects/objinspect)
[![downloads](https://img.shields.io/pepy/dt/objinspect?label=downloads&color=blue&labelColor=30363d)](https://pepy.tech/projects/objinspect)
[![license](https://img.shields.io/github/license/zigai/objinspect?label=license&labelColor=30363d)](LICENSE)

`objinspect` is a high-level wrapper around Python's built-in `inspect` module.
It provides a simple interface for examining Python functions and classes.

## Features

- Inspect functions, methods, and classes with a consistent API
- Access signatures, parameters, return annotations, and docstrings
- `prettydir` (alias: `pdir`) for a richer `dir()`-style view

## Installation

### From PyPI

```sh
pip install objinspect
```

```sh
uv add objinspect
```

### From source

```sh
pip install git+https://github.com/zigai/objinspect
```

```sh
uv add git+https://github.com/zigai/objinspect
```

## Examples

```python
>>> from objinspect import inspect
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
