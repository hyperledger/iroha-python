# Wheel Build Utilities

Here are stored the scripts that help build a wheel for pypi repository:

* `download-schema.py` - downloads Iroha's shared model proto files to schema folder
* `compile-proto.py` - compiles downloaded proto to Python includes format and fixes relative imports for iroha package

**Most likely you do NOT need those scripts.**

Anyway, they can successfully run inside `hyperledger/iroha:develop-build` Docker container.

You may need to build the wheel on your own only in exceptional cases.
Please use `pip install iroha` or `pip install --upgrade iroha` by default.

The wheel itself can be built and installed with:

```bash
cd iroha-python
scripts/download-schema.py
scripts/compile-proto.py
python3 setup.py bdist_wheel
pip install dist/iroha*.whl
```
