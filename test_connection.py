
from connection import Kannagi
from protos.api_pb2 import Transaction

k = Kannagi()
# This sample is bad. so we should create builder
tx = Transaction()

k.torii(tx)

