SHELL := /bin/bash
SCHEMA := schema
PROTO_SCHEMA := schema

all: all-proto

all-proto:
	protoc -I=./ --python_out=./$(PROTO_SCHEMA) ./$(SCHEMA)/*proto
	python -m grpc_tools.protoc -I./ --python_out=./$(PROTO_SCHEMA) --grpc_python_out=./$(PROTO_SCHEMA) ./$(SCHEMA)/endpoint.proto
	# because, correct pre protoc version 3.3.2
	mv -f schema/schema/* schema
