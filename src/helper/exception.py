from __future__ import absolute_import, division, print_function, unicode_literals

class IrohaPythonExceptipn(Exception):
    status_code = 500
    message = "Occured Error"

    def __init__(self, status_code=None, payload=None):
        Exception.__init__(self)
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

"""
    status_code:
        - 510
            HasFieldException
"""
class NotCommandException(IrohaPythonExceptipn):
    status_code = 510
    message = "NotCommandException"

class NotErrorResponseException(IrohaPythonExceptipn):
    status_code = 510
    message = "NotErrorResponseException"

class NotAccountResponseException(IrohaPythonExceptipn):
    status_code = 510
    message = "NotAccountResponseException"

class NotAccountAssetResponseException(IrohaPythonExceptipn):
    status_code = 510
    message = "NotAccountAssetResponseException"

class NotSignatoriesResponseExcepiton(IrohaPythonExceptipn):
    status_code = 510
    message = "NotSignatoriesResponseExcepiton"


class NotTransactionsResponseException(IrohaPythonExceptipn):
    status_code = 510
    message = "NotTransactionsResponseException"
