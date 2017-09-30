from __future__ import absolute_import, division, print_function, unicode_literals

class IrohaPythonExceptipn(Exception):
    message = "Occured Error"

"""
    HasFieldException
"""
class NotCommandException(IrohaPythonExceptipn):
    message = "NotCommandException"

class NotErrorResponseException(IrohaPythonExceptipn):
    message = "NotErrorResponseException"

class NotAccountResponseException(IrohaPythonExceptipn):
    message = "NotAccountResponseException"

class NotAccountAssetResponseException(IrohaPythonExceptipn):
    message = "NotAccountAssetResponseException"

class NotSignatoriesResponseExcepiton(IrohaPythonExceptipn):
    message = "NotSignatoriesResponseExcepiton"


class NotTransactionsResponseException(IrohaPythonExceptipn):
    message = "NotTransactionsResponseException"
