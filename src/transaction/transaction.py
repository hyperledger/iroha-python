from src.helper import logger,crypto

from schema.transaction_pb2 import Transaction as TransactionSchema
from src.primitive.signatories import Signatories

class Transaction:
    def __init__(self):
        logger.info("Create Transaction Constract")
        self.tx = TransactionSchema(
            payload = TransactionSchema.Payload(
                created_time = crypto.now()
            ),
            signatures = []
        )
        self.signatories = Signatories()


    def set_creator_account_id(self,creator_account_id):
        self.tx.payload.creator_account_id = creator_account_id

    def set_tx_counter(self,tx_counter):
        self.tx.payload.tx_counter = tx_counter


    def add_key_pair(self,keypair):
        logger.debug("Transaction.add_key_pair")
        self.signatories.append(keypair)

    def add_key_pairs(self,keypairs):
        logger.debug("Transaction.add_key_pairs")
        for k in keypairs:
            self.signatories.append(k)

    def time_stamp(self):
        logger.debug("Transaction.time_stamp")
        self.tx.payload.created_time = crypto.now()

    def sign(self):
        logger.debug("Transaction.sign")
        self.signatories.sign(self.tx)
        self.signatories.clean()

    def signatures_clean(self):
        logger.debug("Transaction.signatures_clean")
        self.tx.signature = []

    def signatories_clean(self):
        logger.debug("Transaction.signatories_clean")
        self.signatories.clean()
