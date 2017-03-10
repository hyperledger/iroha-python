import protos.api_pb2_grpc as api_pb2_grpc
import grpc


class Kannagi:
    def __init__(self):
        # ToDo configurable
        channel = grpc.insecure_channel('localhost:50051')
        self.sumeragi_stub = api_pb2_grpc.SumeragiStub(channel)
        self.asset_repo_stub = api_pb2_grpc.AssetRepositoryStub(channel)

    def torii(self, tx):
        res = self.sumeragi_stub.Torii(
            tx
        )
        # ToDo  log class
        print("client received: " + res.message)
        return res

    def assetRepository(self, query):
        return self.asset_repo_stub.find(query)
