# Wheel Build Utilities

Here are stored the scripts that help build a wheel for pypi repository:

* `download-schema.py` - downloads Iroha's shared model proto files to schema folder
* `compile-proto.py` - compiles downloaded proto to Python includes format and fixes relative imports for iroha package

**Most likely you do NOT need those scripts.**

Anyway, they can successfully run inside `hyperledger/iroha:develop-build` Docker container.
