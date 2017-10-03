from iroha.helper import logger,crypto

from schema.transaction_pb2 import Transaction as TransactionSchema
from schema.endpoint_pb2 import TxStatusRequest

from iroha.primitive.signatories import Signatories
from iroha.transaction import command as helper_command
from iroha.helper import stateless_validator

class Transaction:
    def __init__(self):
        logger.debug("Create Transaction Construct")
        self.tx = TransactionSchema(
            payload = TransactionSchema.Payload(
                created_time = crypto.now()
            ),
            signatures = []
        )
        self.signatories = Signatories()


    def set_creator_account_id(self,creator_account_id):
        """
        Set creator of this transaction.

        Args:
            creator_account_id ( str ) : it is creator's account id of transaction
        """
        logger.debug("Transaction.set_creator_account_id")
        self.tx.payload.creator_account_id = creator_account_id

    def set_tx_counter(self,tx_counter):
        """
        Set tx counter of this transaction

        Args:
            tx_counter ( int ) : tx_counter is counter of transaction
        """
        logger.debug("Transaction.set_tx_counter")
        self.tx.payload.tx_counter = tx_counter

    def set_connection(self,connection):
        """
        Set connection used to connect iroha

        Args:
            connection ( `Connection` ): connection used to connect iroha
        """
        logger.debug("Transaction.set_connection")
        self.connection = connection

    def add_key_pair(self,keypair):
        """
        Add keypair ( public key and private key generated iroha.keygen() )

        Args:
            keypair ( `KeyPair` ) : keypair generated iroha.keygen()
        """
        logger.debug("Transaction.add_key_pair")
        self.signatories.append(keypair)

    def add_key_pairs(self,keypairs):
        """
        Add keypairs ( public key and private key generated iroha.keygen() )
        Args:
            keypairs ( []`KeyPair` ): array of keypair
        """
        logger.debug("Transaction.add_key_pairs")
        for k in keypairs:
            self.signatories.append(k)

    def time_stamp(self):
        """
        Set current(call this function) time timestamp of this transaction
        """
        logger.debug("Transaction.time_stamp")
        self.tx.payload.created_time = crypto.now()

    def sign(self):
        """
        Do sign to this transaction from this signatories.
        """
        logger.debug("Transaction.sign")
        self.signatories.sign(self.tx)
        self.signatories.clean()

    def signatures_clean(self):
        """
        Delete all signature info. ( So, after call this func number of signatures of transaction is 0 )
        """
        logger.debug("Transaction.signatures_clean")
        while self.tx.signatures.__len__():
            self.tx.signatures.pop()

    def count_signatures(self):
        """
        Count all signatures.
        Returns:
            int: number of this transactions's signatures

        """
        logger.debug("Transaction.count_signatures")
        return self.tx.signatures.__len__()

    def signatories_clean(self):
        """
        Delete all signatories info. ( not delete signatures of transaction info )
        """
        logger.debug("Transaction.signatories_clean")
        self.signatories.clean()

    def hash(self):
        """
        Get hash of this transaction

        Returns:
            bytes: The return value is hash of this transction
        """
        logger.debug("Transaction.hash")
        return crypto.sign_hash(self.tx.payload)

    def verify(self):
        """
        Verify stateless validate this transaction.
        Included signature check.

        Returns:
            bool: The return value. True for success, False otherwise.

        """
        logger.debug("Transaction.verify")
        return stateless_validator.verify(self.tx)

    def add_command(self,cmd):
        """
        Add Command to this transaction
        Args:
            cmd( `CreateAccount`,`AddSignatory`,`RemoveSignatory`,`CreateDomain`,`CreateAsset`,
                `AddAssetQuantity`,`SetAccountQuorum` or `TransferAsset` ): command of protobuf structre.

        """
        logger.debug("add_command")
        self.tx.payload.commands.extend(
            [helper_command.wrap_cmd(cmd)]
        )

    def add_commands(self,cmds):
        """
        Add Commands to this transaction
        Args:
            cmds ( [](`CreateAccount`,`AddSignatory`,`RemoveSignatory`,`CreateDomain`,`CreateAsset`,
                `AddAssetQuantity`,`SetAccountQuorum` or `TransferAsset`) ): array of command type protobuf structre.
        """
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

    def issue(self):
        """
        Issue to iroha with this transaction
        """
        logger.debug("Transaction.issue")
        self.connection.tx_stub().Torii(self.tx)

    def check(self):
        """
        Check this transaction status for iroha
        Returns:
            TxStatusResponse: Transaction Status Code
        """
        logger.debug("Transaction.check")
        # TODO thinking now
        check = TxStatusRequest(
            tx_hash=self.hash()
        )
        return self.connection.tx_stub().Status(check)
