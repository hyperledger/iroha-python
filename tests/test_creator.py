import unittest

from src.helper import logger,crypto
from src.creator import Creator

from schema.transaction_pb2 import Transaction
from schema.primitive_pb2 import Signature

class CreatorTest(unittest.TestCase):
    def setUp(self):
        logger.setDebug()
        logger.info("CreatorTest")

    def test_creator(self):
        creator = Creator()

        keypairs = []
        keypairs.append(crypto.create_key_pair())
        keypairs.append(crypto.create_key_pair())


        creator.set_account_id("test@test")
        creator.set_keys(keypairs)

        tx = creator.create_tx()
        tx.sign()
        self.assertEqual(
            tx.debug_proto_transaction(),
            Transaction(
                payload = Transaction.Payload(
                    creator_account_id = "test@test",
                    created_time = tx.debug_proto_transaction().payload.created_time
                ),
                signatures = [
                    Signature(
                        pubkey = keypairs[0].public_key,
                        signature = crypto.sign(
                            keypairs[0],
                            crypto.sign_hash(tx.debug_proto_transaction().payload)
                        )
                    ),
                    Signature(
                        pubkey = keypairs[1].public_key,
                        signature = crypto.sign(
                            keypairs[1],
                            crypto.sign_hash(tx.debug_proto_transaction().payload)
                        )
                    )
                ]
            )
        )

