# iroha-python
Python library for Hyperledger Iroha.

# Compile proto
```
cd protoc; protoc --python_out=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_python_plugin` api.proto
```

