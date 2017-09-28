from src.helper import crypto
import base64
import sha3
import unittest

from schema.transaction_pb2 import Transaction
from schema.primitive_pb2 import Signature
from schema.commands_pb2 import Command
from src.helper import logger

class CryptTest(unittest.TestCase):

    def setUp(self):
        self.keypair = crypto.create_key_pair()

        create_ac = Command.CreateAccount(
            account_name = "rihito",
            domain_id = "light.wing",
            main_pubkey = self.keypair.public_key
        )
        self.payload = Transaction.Payload(
            commands = [
                Command(create_account = create_ac)
            ],
            creator_account_id = "rihito@light.wing",
            tx_counter = 0,
            created_time = crypto.now()
        )

        self.tx = Transaction(
            payload = self.payload,
            signatures = [
                Signature(
                    pubkey = self.keypair.public_key,
                    signature = crypto.sign(self.keypair,crypto.sign_hash(self.payload))
                )
            ]
        )

    def test_sign_hash(self):
        hash = crypto.sign_hash(self.tx.payload)

        logger.info(hash)
        logger.info(crypto.b64encode(hash))

        sign = crypto.sign(self.keypair,hash)

        logger.info(sign)

        is_verify = crypto.verify(self.keypair.public_key,sign,hash)

        logger.info(is_verify)
        self.assertTrue(is_verify)


    def test_time(self):
        logger.info(crypto.now())
