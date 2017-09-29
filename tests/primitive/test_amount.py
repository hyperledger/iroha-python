import unittest

from src.helper import logger
from src.primitive import amount


class CipherTest(unittest.TestCase):
    def test_amount_changer(self):
        logger.info("test_amount_changer")
        logger.setDebug()


        logger.debug(10000000000000000000*100000000000000000000 + 1000)

        num = int(3121092321831273291731287318721973219)
        amnt = amount.int2amount(num, 2)
        logger.debug(amnt)
        re_num = amount.amount2int(amnt)
        self.assertEqual(num,re_num)

    def test_amount_changer_2(self):
        logger.info("test_amount_changer")
        logger.setDebug()
        num = int(11210923218312732917312873187219732193219032178323213921738193687287361873872)
        amnt = amount.int2amount(num, 2)
        logger.debug(amnt)
        re_num = amount.amount2int(amnt)
        self.assertEqual(num,re_num)
