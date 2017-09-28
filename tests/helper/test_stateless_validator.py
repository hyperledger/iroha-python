import unittest

from schema.transaction_pb2 import Transaction
from schema.commands_pb2 import Command
from schema.primitive_pb2 import Signature, Amount
from schema.response_pb2 import Query, GetAccount, GetAccountTransactions, GetAccountAssets, GetAccountAssetTransactions, GetSignatories, GetTransactions

from src.helper import crypto, logger, stateless_validator

class TestCommand(unittest.TestCase):

    def setUp(self):
        self.creator = "chika@ichigo.mashimaro"
        self.keypair = crypto.create_key_pair()
        self.tx_counter = 0
        logger.setDebug()

    def test_stateless_validator_true(self):
        logger.debug("test_create_account")
        create_ac = Command.CreateAccount(
            account_name = "rihito",
            domain_id = "light.wing",
            main_pubkey = self.keypair.public_key
        )
        payload = Transaction.Payload(
            commands = [
                Command(create_account = create_ac)
            ],
            creator_account_id = self.creator,
            tx_counter = self.tx_counter,
            created_time = crypto.now()
        )

        tx = Transaction(
            payload = payload,
            signatures = [
                Signature(
                    pubkey = self.keypair.public_key,
                    signature = crypto.sign(self.keypair,crypto.sign_hash(payload))
                )
            ]
        )
        self.assertTrue(stateless_validator.verify(tx))

    def test_stateless_validator_created_at_ng(self):
        logger.debug("test_stateless_validator_created_at_ng")
        create_ac = Command.CreateAccount(
            account_name = "rihito",
            domain_id = "light.wing",
            main_pubkey = self.keypair.public_key
        )
        payload = Transaction.Payload(
            commands = [
                Command(create_account = create_ac)
            ],
            creator_account_id = self.creator,
            tx_counter = self.tx_counter,
            created_time = crypto.now()-3600*24*1000*10
        )

        tx = Transaction(
            payload = payload,
            signatures = [
                Signature(
                    pubkey = self.keypair.public_key,
                    signature = crypto.sign(self.keypair,crypto.sign_hash(payload))
                )
            ]
        )
        self.assertFalse(stateless_validator.verify(tx))

        payload = Transaction.Payload(
            commands = [
                Command(create_account = create_ac)
            ],
            creator_account_id = self.creator,
            tx_counter = self.tx_counter,
            created_time = crypto.now()+3600*24*1000*10
        )

        tx = Transaction(
            payload = payload,
            signatures = [
                Signature(
                    pubkey = self.keypair.public_key,
                    signature = crypto.sign(self.keypair,crypto.sign_hash(payload))
                )
            ]
        )
        self.assertFalse(stateless_validator.verify(tx))


    def test_stateless_validator_signature_ng(self):
        logger.debug("test_stateless_validator_signature_ng")

        create_ac = Command.CreateAccount(
            account_name = "rihito",
            domain_id = "light.wing",
            main_pubkey = self.keypair.public_key
        )
        payload = Transaction.Payload(
            commands = [
                Command(create_account = create_ac)
            ],
            creator_account_id = self.creator,
            tx_counter = self.tx_counter,
            created_time = crypto.now()
        )
        payload2 = Transaction.Payload(
            commands = [
                Command(create_account = create_ac)
            ],
            creator_account_id = self.creator,
            tx_counter = self.tx_counter,
            created_time = crypto.now()+1
        )
        tx = Transaction(
            payload = payload,
            signatures = [
                Signature(
                    pubkey = self.keypair.public_key,
                    signature = crypto.sign(self.keypair,crypto.sign_hash(payload2))
                )
            ]
        )
        self.assertFalse(stateless_validator.verify(tx))




    def test_stateless_validator_create_account(self):
        create_ac = Command(
            create_account = Command.CreateAccount(
                account_name = "rihito",
                domain_id = "light.wing",
                main_pubkey = self.keypair.public_key
            )
        )
        self.assertTrue(stateless_validator.command(create_ac))
        create_ac = Command(
            create_account = Command.CreateAccount(
                account_name = "rihitoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
                domain_id = "light.wing",
                main_pubkey = self.keypair.public_key
            )
        )
        self.assertFalse(stateless_validator.command(create_ac))
        create_ac = Command(
            create_account = Command.CreateAccount(
                account_name = "rihito",
                domain_id = "light.wing.a.c.f",
                main_pubkey = self.keypair.public_key
            )
        )
        self.assertTrue(stateless_validator.command(create_ac))
        create_ac = Command(
            create_account = Command.CreateAccount(
                account_name = "rihito",
                domain_id = "light.wing.a*.c.d.e.f.g.sf",
                main_pubkey = self.keypair.public_key
            )
        )
        self.assertFalse(stateless_validator.command(create_ac))


    def test_stateless_validator_add_signatory(self):
        add_sig = Command(
            add_signatory = Command.AddSignatory(
                account_id = "rihito@light.wing",
                pubkey = self.keypair.public_key
            )
        )
        self.assertTrue(stateless_validator.command(add_sig))

    def test_stateless_validator_set_account_quorum(self):
        set_ac_q = Command(
            set_account_quorum = Command.SetAccountQuorum(
                account_id = "rihito@light.wing",
                quorum = 100
            )
        )
        self.assertTrue(stateless_validator.command(set_ac_q))
        set_ac_q = Command(
            set_account_quorum = Command.SetAccountQuorum(
                account_id = "rihito@light.wing",
                quorum = 0
            )
        )
        self.assertFalse(stateless_validator.command(set_ac_q))


    def test_stateless_validator_create_domain(self):
        create_d = Command(
            create_domain = Command.CreateDomain(
                domain_name="ichigo.mashimaro"
            )
        )
        self.assertTrue(stateless_validator.command(create_d))
        create_d = Command(
            create_domain = Command.CreateDomain(
                domain_name="ichigo+mashimaro"
            )
        )
        self.assertFalse(stateless_validator.command(create_d))


    def test_stateless_validator_create_asset(self):
        create_as = Command(
            create_asset = Command.CreateAsset(
                asset_name="yen",
                domain_id="ichigo.mashimaro",
                precision=3
            )
        )
        self.assertTrue(stateless_validator.command(create_as))


    def test_stateless_validator_add_asset_quantity(self):
        add_asset_q = Command(
            add_asset_quantity = Command.AddAssetQuantity(
                account_id="chika@ichigo.mashimaro",
                asset_id="ichigo.mashimaro/yen",
                amount=Amount(
                    integer_part=100,
                    fractial_part=0
                )
            )
        )
        self.assertTrue(stateless_validator.command(add_asset_q))
        add_asset_q = Command(
            add_asset_quantity = Command.AddAssetQuantity(
                account_id="chika@ichigo.mashimaro",
                asset_id="ichigo.mashimaro/",
                amount=Amount(
                    integer_part=100,
                    fractial_part=0
                )
            )
        )
        self.assertFalse(stateless_validator.command(add_asset_q))

    def test_stateless_validator_transfer_asset(self):
        transfer_as = Command(
            transfer_asset = Command.TransferAsset(
                src_account_id="chika@ichigo.mashimaro",
                dest_account_id="miu@ichigo.mashimaro",
                asset_id="ichigo.mashimaro/yen",
                amount=Amount(
                    integer_part=100,
                    fractial_part=0
                )
            )
        )
        self.assertTrue(stateless_validator.command(transfer_as))


    def test_stateless_query(self):
        query = Query(
            payload = Query.Payload (
                creator_account_id = "satoshi@pokemon",
                created_time = crypto.now(),
                get_account = GetAccount(
                    account_id = "satoshi@pokemon"
                )
            )
        )
        self.assertTrue(stateless_validator.query(query))
        query.payload.created_time = 0
        self.assertFalse(stateless_validator.query(query))

    def test_stateless_get_transactions(self):
        create_ac = Command.CreateAccount(
            account_name = "rihito",
            domain_id = "light.wing",
            main_pubkey = self.keypair.public_key
        )
        payload = Transaction.Payload(
            commands = [
                Command(create_account = create_ac)
            ],
            creator_account_id = self.creator,
            tx_counter = self.tx_counter,
            created_time = crypto.now()-3600*24*1000*10
        )

        get_txs = GetTransactions(
            tx_hashes = [
                crypto.sign_hash(payload)
            ]
        )
        self.assertTrue(stateless_validator.get_transactions(get_txs))
        get_txs = GetTransactions(
            tx_hashes = [
                b"aaaaa0000000"
            ]
        )
        self.assertFalse(stateless_validator.get_transactions(get_txs))
