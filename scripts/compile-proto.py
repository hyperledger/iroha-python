#!/usr/bin/env python3

from six.moves import getoutput
import os.path
from os import chdir

directory = os.path.dirname(os.path.abspath(__file__))
chdir(directory)
print('Working directory set to {}'.format(directory))

proto_path = os.path.join('..', 'schema')
python_out = os.path.join('..', 'iroha')
out_pb2 = os.path.join(python_out, '*pb2*.py')
protos = os.path.join(proto_path, '*.proto')
endpoint_proto = os.path.join(proto_path, 'endpoint.proto')

print(getoutput('protoc --proto_path={} --python_out={} {}'.
                format(proto_path, python_out, protos)))
print(getoutput('python -m grpc_tools.protoc --proto_path={} \
	--python_out={} --grpc_python_out={} {}'.
                format(proto_path, python_out, python_out, endpoint_proto)))

print(getoutput('sed -i.bak \'s/^\\(import.*_pb2\\)/from . \\1/\' {}'.
                format(out_pb2)))
print('Done.')
