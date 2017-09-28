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
        self.stub_tx = self.__get_command_stub(channel)
        self.stub_query = self.__get_query_stub(channel)


    def __get_command_stub(self,channel):
        return CommandServiceStub(channel)

    def __get_query_stub(self,channel):
        return QueryServiceStub(channel)
