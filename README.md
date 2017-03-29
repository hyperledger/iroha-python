# iroha-python [![CircleCI](https://img.shields.io/circleci/project/github/hyperledger/iroha-python/master.svg)](https://circleci.com/gh/hyperledger/iroha-python/tree/master)

Python library for [Hyperledger Iroha](https://github.com/hyperledger/iroha).

## Install

### Python

Supported Python versions: 2.7 and 3.5 (see `tox.ini`).
Multiple Python versions can be installed with your system package manager or with the [pyenv](https://github.com/pyenv/pyenv) tool.
The pyenv itself can also be installed with a system package manager or with the [pyenv-installer](https://github.com/pyenv/pyenv-installer) script.

#### Example installation steps

```sh
# Install pyenv using pyenv-installer
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
# pyenv initialization
export PATH="${HOME}/.pyenv/bin:${PATH}"
eval "$(pyenv init -)"
# Also initialize on startup; if you are using zsh, replace "~/.bashrc" with "~/.zshrc"
echo 'export PATH="${HOME}/.pyenv/bin:${PATH}"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
# Install the most recent Python versions (both 3 and 2)
pyenv install 3.5.2
pyenv install 2.7.13
# Bring both installed versions into the scope: we are testing against both versions
pyenv global 3.5.2 2.7.13
# Only the "tox" package needs to be installed manually
pip install tox
```

### External dependencies

Download [FlatBuffers](https://github.com/google/flatbuffers), compile the `flatc` executable and place it into your `PATH`.

`.circleci/config.yml` contains working build commands.
These commands might need some adaptation to your local environment.

## Develop

### First-time setup

Run `python setup.py genfbs` to generate the FlatBuffers schema.

### Interactive shell

Run `tox -e dev` to get an [IPython shell](https://ipython.org/) in a virtual environment with all dependencies installed.

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
