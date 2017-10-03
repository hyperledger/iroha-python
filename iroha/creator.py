"""Python library for Hyperledger Iroha."""


from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from iroha.helper import logger
from iroha.transaction.transaction import Transaction
from iroha.query.query import Query

class Creator:
    """
    Creator is Account for creating transaction or query.
    Creator has account_id, signatories and connection(used to connect iroha).
    """
    def __init__(self,account_id=None, keys=None, connection=None):
        """
        Initialize Creator info

        Args:
            account_id ( str ): creator's account_id (e.g : "account@domain.com")
            keys ( []`KeyPair` ): array of `KeyPair`. There are signatories of this creator.
            connection ( `Connection` ): connection used to connect iroha.
        """
        logger.debug("Construct Creator")
        self.set_account_id(account_id)
        self.set_keys(keys)
        self.set_connection(connection)

    def set_account_id(self, account_id):
        """
        Set creator account id

        Args:
            account_id ( str ): creator account id
        """
        logger.debug("Creator.set_account_id")
        self.creator_account_id = account_id


    def set_keys(self, keys):
        """
        Set keypairs (means signatoiers) of creator
        Args:
            keys ( []`KeyPair` ): array of keypair ( public key and private key )
        """
        logger.debug("Creator.set_keys")
        self.signatories = keys

    def set_connection(self,connection):
        """
        Set Connection used to connect iroha
        Args:
            connection ( `Connect` ): connection used to connect iroha
        """
        logger.debug("Creator.set_connection")
        self.connection = connection

    def create_tx(self):
        """
        Create Transaction

        Returns:
            `Transaction`: created transaction with added signatory, account_id, time stamp, and connection
        """
        logger.debug("Creator.create_tx")
        retx = Transaction()
        if self.connection:
            retx.set_connection(self.connection)
        if self.signatories:
            retx.add_key_pairs(self.signatories)
        if self.creator_account_id:
            retx.set_creator_account_id(self.creator_account_id)
        # TODO It has not deceided yet
        retx.set_tx_counter(0)
        retx.time_stamp()
        return retx

    def create_query(self):
        """
        Create Query

        Returns:
            `Query`: created query with added account_id, tima stamp, and connection.

        """
        logger.debug("Creator.create_query")
        retq = Query()
        if self.connection:
            retq.set_connection(self.connection)
        if self.creator_account_id:
            retq.set_creator_account_id(self.creator_account_id)
        # TODO It has not deceided yet
        retq.set_query_counter(0)
        retq.time_stamp()
        return retq
