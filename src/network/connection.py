import grpc
from schema.endpoint_pb2 import CommandServiceStub, QueryServiceStub
from src.helper import logger

class Connection:
    def __init__(self):
        logger.info("Constract Conncection")

    def setUp(self,ip,port):
        self.ip = ip
        self.port = port
        channel = grpc.insecure_channel(ip + ':' + port)
        self.stub_tx = __GetCommandStub(channel)
        self.stub_query = __GetQueryStub(channel)


    def __GetCommandStub(self,channel):
        return CommandServiceStub(channel)

    def __GetQueryStub(self,channel):
        return QueryServiceStub(channel)
