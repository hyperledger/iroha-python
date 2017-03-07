

import protos.api_pb2 as api_pb2
import protos.api_pb2_grpc as api_pb2_grpc
import grpc

class Kannagi:

  def __init__(self):
    # ToDo configurable
    channel = grpc.insecure_channel('localhost:50051')
    self.stub = api_pb2_grpc.SumeragiStub(channel)

  def torii(self, tx):
    res = self.stub.Torii(
      tx
    )
    # ToDo  log class
    print("client received: " + res.message)
    return res


