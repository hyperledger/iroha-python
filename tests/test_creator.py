import unittest

from iroha.helper import logger,crypto
from iroha.creator import Creator

from schema.transaction_pb2 import Transaction
from schema.response_pb2 import Query
from schema.primitive_pb2 import Signature

class CreatorTest(unittest.TestCase):
    def setUp(self):
        logger.setDebug()
        logger.info("CreatorTest")

    def test_create_tx(self):
        logger.info("test_create_tx")
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
                signature = [
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

    def test_create_query(self):
        logger.info("test_create_query")
        creator = Creator()

        creator.set_account_id("taiyo@blue.player")

        query = creator.create_query()
        self.assertEqual(
            query.debug_proto_query(),
            Query(
                payload = Query.Payload(
                    creator_account_id = "taiyo@blue.player",
                    created_time = query.debug_proto_query().payload.created_time
                )
            )
        )


