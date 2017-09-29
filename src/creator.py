"""Python library for Hyperledger Iroha."""


from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from src.helper import logger
from src.transaction.transaction import Transaction

class Creator:
    def __init__(self):
        logger.info("Construct Creator")

    def set_account_id(self, account_id):
        logger.debug("Creator.set_account_id")
        self.creator_account_id = account_id

    def set_keys(self, keys):
        logger.debug("set_keys")
        self.signatories = keys

    def create_tx(self):
        logger.debug("create_tx")
        retx = Transaction()
        retx.add_key_pairs(self.signatories)
        retx.set_creator_account_id(self.creator_account_id)
        retx.time_stamp()
        return retx
