# iroha-python
Python library for Hyperledger Iroha.

# Compile proto
```
cd protoc; python -m grpc_tools.protoc -I../../protos --python_out=. --grpc_python_out=. api.proto
```

