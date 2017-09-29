from src.helper import logger,crypto

from schema.transaction_pb2 import Transaction as TransactionSchema

from src.primitive.signatories import Signatories
from src.transaction import command as helper_command
from src.helper import stateless_validator

class Transaction:
    def __init__(self):
        logger.info("Create Transaction Construct")
        self.tx = TransactionSchema(
            payload = TransactionSchema.Payload(
                created_time = crypto.now()
            ),
            signatures = []
        )
        self.signatories = Signatories()


    def set_creator_account_id(self,creator_account_id):
        logger.debug("Transaction.set_creator_account_id")
        self.tx.payload.creator_account_id = creator_account_id

    def set_tx_counter(self,tx_counter):
        logger.debug("Transaction.set_tx_counter")
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
        while self.tx.signatures.__len__():
           self.tx.signatures.pop()

    def count_signatures(self):
        logger.debug("Transaction.count_signatures")
        return self.tx.signatures.__len__()

    def signatories_clean(self):
        logger.debug("Transaction.signatories_clean")
        self.signatories.clean()

    def hash(self):
        logger.debug("Transaction.hash")
        return crypto.sign_hash(self.tx.payload)

    def verify(self):
        logger.debug("Transaction.verify")
        return stateless_validator.verify(self.tx)

    def add_command(self,cmd):
        logger.debug("add_command")
        self.tx.payload.commands.extend(
            [helper_command.wrap_cmd(cmd)]
        )

    def add_commands(self,cmds):
        logger.debug("add_commands")
        wcmds = []
        for cmd in cmds:
            wcmds.append(helper_command.wrap_cmd(cmd))
        self.tx.payload.commands.extend(
            [wcmds]
        )

    def debug_proto_transaction(self):
        logger.debug("debug_porto_transaction")
        return self.tx
