from __future__ import absolute_import, division, print_function, unicode_literals
from iroha.helper import logger

class IrohaPythonException(Exception):
    message = "Occured Error"
    def __init__(self,option=None):
        logger.warning(self.message)
        if option:
            logger.warning(option)

"""
    HasFieldException
"""
class NotCommandException(IrohaPythonException):
    message = "NotCommandException"

class NotErrorResponseException(IrohaPythonException):
    message = "NotErrorResponseException"

class NotAccountResponseException(IrohaPythonException):
    message = "NotAccountResponseException"

class NotAccountAssetResponseException(IrohaPythonException):
    message = "NotAccountAssetResponseException"

class NotSignatoriesResponseExcepiton(IrohaPythonException):
    message = "NotSignatoriesResponseExcepiton"


class NotTransactionsResponseException(IrohaPythonException):
    message = "NotTransactionsResponseException"


class InvalidIpException(IrohaPythonException):
    message = "InvalidIpException"

class InvalidPortException(IrohaPythonException):
    message = "InvalidPortException"

class NotConnectionStubException(IrohaPythonException):
    message = "NotConnectionStubException"
