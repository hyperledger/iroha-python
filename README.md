# iroha-python

Python library for [Hyperledger Iroha](https://github.com/hyperledger/iroha).


## Install

Supported Python versions: 2.7 and 3.6 (see `tox.ini`).
Multiple Python versions can be installed with your system package manager or with the [pyenv](https://github.com/pyenv/pyenv) tool.

## Develop

### New dependencies

After adding a new dependency, include it into the `install_requires` option of the `setup.py` script.

### Python 2 compatibility

Familiarize yourself with the Python compatibility guidelines and supporting packages:

* [Porting Python 2 Code to Python 3](https://docs.python.org/3/howto/pyporting.html)
* [Writing code that runs under both Python2 and 3](https://wiki.python.org/moin/PortingToPy3k/BilingualQuickRef)
* The [future](http://python-future.org) package
* The [six](http://pythonhosted.org/six) package

Put the following at the top of all your Python files (after a docstring and file-wide comments):

```python
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
```

## Test

[tox](http://tox.readthedocs.io) tests the package under different virtual environments and with different Python versions.
Simply execute the `tox` command to run all tests in all supported environments.

## Compile proto
```
cd protoc; python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. api.proto
```

**\*Future replace protobuf with flatbuffer \('A')/**
