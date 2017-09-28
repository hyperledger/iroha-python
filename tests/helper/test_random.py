import unittest
from src.helper import random
from src.helper import logger

class TestRandom(unittest.TestCase):

    def test_random(self):
        a = random.uuid(10)
        self.assertTrue(len(a),10)
        b = random.uuid(53)
        self.assertTrue(len(b),53)
        logger.debug(a)
        logger.debug(b)