# iroha-python

Python library for Hyperledger Iroha.


## Install

Install [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io).

```sh
git clone https://github.com/hyperledger/iroha-python.git
cd iroha-python
mkvirtualenv iroha-python
workon iroha-python
pip install -r requirements.txt
```

If you are using anaconda:

```sh
conda create -n iroha-python python=3.6
source activate iroha-python
```

## Develop

After adding a new dependency:

```sh
pip freeze > requirements.txt
```

Do this in every module:

```python
from __future__ import division, print_function, unicode_literals
```

## Test

```sh
tox
```

## Compile proto
```
cd protoc; python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. api.proto
```

**\*Future replace protobuf with flatbuffer \('A')/**

