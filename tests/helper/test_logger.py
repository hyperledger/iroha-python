import unittest
from iroha.helper import logger

class LoggerTest(unittest.TestCase):
    def test_logger_debug(self):
        logger.debug("debug message")

    def test_logger_warning(self):
        logger.warning("warning message")

    def test_logger_info(self):
        logger.info("info message")
