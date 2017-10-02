"""Python library for Hyperledger Iroha."""


from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from src.helper import logger
from src.transaction.transaction import Transaction
from src.query.query import Query

class Creator:
    def __init__(self,account_id, keys, connection):
        logger.info("Construct Creator")
        self.set_account_id(account_id)
        self.set_keys(keys)
        self.set_connection(connection)

    def set_account_id(self, account_id):
        logger.debug("Creator.set_account_id")
        self.creator_account_id = account_id

    def set_keys(self, keys):
        logger.debug("Creator.set_keys")
        self.signatories = keys

    def set_connection(self,connection):
        logger.debug("Creator.set_connection")
        self.connection = connection

    def create_tx(self):
        logger.debug("Creator.create_tx")
        retx = Transaction()
        retx.add_key_pairs(self.signatories)
        retx.set_creator_account_id(self.creator_account_id)
        retx.time_stamp()
        return retx

    def create_query(self):
        logger.debug("Creator.create_query")
        retq = Query()
        retq.set_creator_account_id(self.creator_account_id)
        retq.time_stamp()
        return retq
