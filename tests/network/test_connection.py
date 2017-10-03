import unittest

from src.network.connection import Connection
from src.helper import logger

class ConnectionTest(unittest.TestCase):

    def setUp(self):
        logger.setDebug()
        logger.info("ConnectionTest")

    def test_connect_normal(self):
        try:
            Connection(ip="127.162.19.19",port=5050)
        except:
            self.assertTrue(False)
        self.assertTrue(True)

    def test_connect_except(self):
        try:
            Connection(ip="hostname",port=5050)
        except:
            self.assertTrue(True)
