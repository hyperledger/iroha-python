import grpc
from schema.endpoint_pb2 import CommandServiceStub, QueryServiceStub
from src.helper import logger, stateless_validator, exception

class Connection:
    """
    Connection has managed to connection to iroha.
    """
    def __init__(self,**connection_env):
        """
        Connection establish to iroha.
        If connection_env is empty, nothing to do.

        :param connection_env:
            ip = ip address string of iroha. ( default "0.0.0.0" )
            port = port number string of iroha. (default : "8080" )
        """
        logger.info("Constract Conncection")
        self.ip = "0.0.0.0"
        self.port = "8080"
        if "ip" in connection_env and "port" in connection_env:
            self.set_env(connection_env)
            self.gen_stub()


    def set_env(self,**connection_env):
        """
        Set environemnt of connect iroha

        :param connection_env:
            ip = ip address string of iroha. ( default "0.0.0.0" )
            port = port number string of iroha. (default : "8080" )
        """
        ip = connection_env["ip"]
        port = connection_env["port"]
        if type(ip) != type(""):
            raise exception.InvalidIpException(ip)
        if not stateless_validator.verify_ip(ip):
            raise exception.InvalidIpException(ip)
        if type(connection_env["port"] != type("")):
            raise exception.InvalidPortException(port)
        if not stateless_validator.verify_port(port):
            raise exception.InvalidPortException(port)

        self.ip = ip
        self.prot = port

    def gen_stub(self):
        """
        Generate Stub for connection to iroha.

        :except It is called, when failed connect or another error.
        """
        channel = grpc.insecure_channel(self.ip + ':' + self.port)
        self.stub_tx = self.__get_command_stub(channel)
        self.stub_query = self.__get_query_stub(channel)

    def tx_stub(self):
        """
        Get Transaction Connection Stub

        :return: transaction service stub
        """
        return self.stub_tx

    def query_stub(self):
        """
        Get Query Connection Stub

        :return: query service stub
        """
        return self.stub_query


    def __get_command_stub(self,channel):
        return CommandServiceStub(channel)

    def __get_query_stub(self,channel):
        return QueryServiceStub(channel)
