import unittest

from src.helper import logger,crypto
from src.transaction.transaction import Transaction

from schema.commands_pb2 import Command

class TransactionTest(unittest.TestCase):
    def setUp(self):
        logger.setDebug()
        logger.debug("TransactionTest")

    def test_transaction(self):
        logger.debug("test_transaction")
        tx = Transaction()

        keypairs = []
        keypairs.append(crypto.create_key_pair())
        keypairs.append(crypto.create_key_pair())
        keypairs.append(crypto.create_key_pair())

        tx.add_key_pairs(keypairs)
        tx.set_creator_account_id("test@test")


        logger.info("add command")
        tx.add_command(
            Command.AddSignatory(
                account_id = "test@test",
                pubkey = keypairs[0].public_key
            )
        )
        tx.add_command(
            Command.SetAccountQuorum(
                account_id = "test@test",
                quorum = 2
            )
        )


        logger.info("check signatures")
        self.assertEqual(tx.count_signatures(),0)
        tx.sign()
        self.assertEqual(tx.count_signatures(),3)
        self.assertTrue(tx.verify())

        tx.add_key_pair(crypto.create_key_pair())
        tx.sign()
        self.assertEqual(tx.count_signatures(),4)
        self.assertTrue(tx.verify())

        tx.time_stamp()
        tx.add_key_pair(crypto.create_key_pair())
        tx.sign()
        self.assertFalse(tx.verify())

        tx.signatures_clean()
        self.assertEqual(tx.count_signatures(),0)
        self.assertEqual(tx.signatories.size(),0)
        self.assertTrue(tx.verify())

        tx.add_command(
            Command.AddSignatory(
                account_id = "test@test",
                pubkey = b"00"
            )
        )
        tx.add_key_pairs(keypairs)
        tx.sign()
        self.assertFalse(tx.verify())
