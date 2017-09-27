"""Python library for Hyperledger Iroha."""


from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from src.helper import logger

class Creator:
    def __init__(self):
        logger.info("Constract Creator")

    def setAccountId(self,account_id):
        self.creator_account_id = account_id

    def setKeys(self,keys):
        self.signatories = keys
