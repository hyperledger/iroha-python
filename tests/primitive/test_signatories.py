import unittest

from iroha.helper import logger,crypto
from iroha.primitive.signatories import Signatories

from schema.transaction_pb2 import Transaction

class PrimitiveTest(unittest.TestCase):
    def setUp(self):
        logger.setDebug()
        logger.debug("PrimitiveTest")

    def test_signatories(self):
        signatories = Signatories()

        keypairs = []
        keypairs.append(crypto.create_key_pair())
        keypairs.append(crypto.create_key_pair())
        keypairs.append(crypto.create_key_pair())

        for key in keypairs:
            signatories.append(key)

        self.assertTrue(signatories.size() == 3)


        tx = Transaction(
            payload = Transaction.Payload(
                creator_account_id = "test@test"
            ),
            signatures = []
        )

        signatories.sign(tx)

        self.assertEqual(len(tx.signatures),3)
        for i in range(0,3):
            sig = tx.signatures[i]
            self.assertTrue(
                crypto.verify(
                    sig.pubkey,
                    sig.signature,
                    crypto.sign_hash(tx.payload)
                )
            )

            self.assertEqual(
                sig.signature,
                crypto.sign(
                    keypairs[i],
                    crypto.sign_hash(tx.payload)
                )
            )

        signatories.clean()
        self.assertEqual(signatories.size(),0)
