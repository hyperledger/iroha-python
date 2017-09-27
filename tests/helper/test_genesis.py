from src.helper import genesis
import unittest

class TestGenesis(unittest.TestCase):

    def setUp(self):
        self.path = "tests/helper/test_zero.tx"

    def test_get_genesis_transaction(self):
        data = genesis.getGenesisTransaction(self.path)
        print( data )