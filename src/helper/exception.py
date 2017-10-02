from __future__ import absolute_import, division, print_function, unicode_literals

class IrohaPythonException(Exception):
    message = "Occured Error"

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
