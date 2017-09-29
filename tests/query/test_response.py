from schema.response_pb2 import AccountResponse, AccountAssetResponse, QueryResponse, TransactionsResponse, ErrorResponse, SignatoriesResponse
from schema.response_pb2 import Account, AccountAsset
from schema.primitive_pb2 import Signature
from schema.transaction_pb2 import Transaction
from src.helper import logger, crypto
from src.primitive.amount import int2amount
from src.query.response import Response

import unittest


class RequestTest(unittest.TestCase):
    def setUp(self):
        logger.setInfo()
        logger.info("RequestTest")
        self.keyapir = crypto.create_key_pair()

    def test_account_response(self):
        logger.debug("test_account_response")
        payload = QueryResponse.Payload(
            account_response = AccountResponse(
                account = Account(
                    account_id = "utishiba@sporing.salt",
                    domain_name = "sporting.salt",
                    quorum = 2
                )
            )
        )
        res = self.helper_make_response(payload)
        self.assertTrue(res.verify())
        self.assertTrue(res.has_account())
        self.assertFalse(res.has_error())
        self.assertEqual(
            res.account(),
            Account(
                account_id="utishiba@sporing.salt",
                domain_name="sporting.salt",
                quorum=2
            )
        )

    def test_account_asset_response(self):
        logger.debug("test_account_asset_response")
        payload = QueryResponse.Payload(
            account_assets_response=AccountAssetResponse(
                account_asset=AccountAsset(
                    asset_id = "sporting.salt/CupNoodles",
                    account_id="utishiba@sporing.salt",
                    balance=int2amount(100,0)
                )
            )
        )
        res = self.helper_make_response(payload)
        self.assertTrue(res.verify())
        self.assertTrue(res.has_account_asset())
        self.assertFalse(res.has_error())
        self.assertEqual(
            res.account_asset(),
            AccountAsset(
                asset_id="sporting.salt/CupNoodles",
                account_id="utishiba@sporing.salt",
                balance=int2amount(100, 0)
            )
        )

    def test_signatories_response(self):
        logger.debug("test_signatories_response")
        payload = QueryResponse.Payload(
            signatories_response = SignatoriesResponse(
                keys = [
                    self.keyapir.public_key
                ]
            )
        )
        res = self.helper_make_response(payload)
        self.assertTrue(res.verify())
        self.assertTrue(res.has_signatories())
        self.assertFalse(res.has_error())
        self.assertEqual(
            res.signatories(),
            [
                self.keyapir.public_key
            ]
        )

    def test_transactions_response(self):
        logger.debug("test_transactions_response")
        payload = QueryResponse.Payload(
            transactions_response = TransactionsResponse(
                transactions = [
                    Transaction(
                        payload = Transaction.Payload(
                            creator_account_id = "koooo@hyoka",
                            created_time = 1145141919
                        )
                    ),
                    Transaction(
                        payload=Transaction.Payload(
                            creator_account_id="yaju@inm",
                            created_time=810893700
                        )
                    )
                ]
            )
        )
        res = self.helper_make_response(payload)
        self.assertTrue(res.verify())
        self.assertTrue(res.has_transactions())
        self.assertFalse(res.has_error())
        self.assertEqual(
            res.transactions(),
            [
                Transaction(
                    payload=Transaction.Payload(
                        creator_account_id="koooo@hyoka",
                        created_time=1145141919
                    )
                ),
                Transaction(
                    payload=Transaction.Payload(
                        creator_account_id="yaju@inm",
                        created_time=810893700
                    )
                )
            ]
        )

    def test_error_response(self):
        logger.debug("test_signatories_response")
        payload = QueryResponse.Payload(
            error_response = ErrorResponse(
                reason = ErrorResponse.NO_ACCOUNT
            )
        )
        res = self.helper_make_response(payload)
        self.assertTrue(res.verify())
        self.assertTrue(res.has_error())
        self.assertFalse(res.has_transactions())
        self.assertEqual(
            res.error_response(),
            ErrorResponse(
                reason=ErrorResponse.NO_ACCOUNT
            )
        )

    def test_verify_response(self):
        logger.debug("test_signatories_response")
        payload = QueryResponse.Payload(
            error_response = ErrorResponse(
                reason = ErrorResponse.NO_ACCOUNT
            )
        )
        res = Response(
            QueryResponse(
                payload=payload,
                signature=Signature(
                    pubkey=self.keyapir.public_key,
                    signature=crypto.sign(self.keyapir, b"ng")
                )
            )
        )
        self.assertFalse(res.verify())


    def helper_make_response(self,payload):
        return Response(
            QueryResponse(
                payload=payload,
                signature=Signature(
                    pubkey=self.keyapir.public_key,
                    signature=crypto.sign(self.keyapir, crypto.sign_hash(payload))
                )
            )
        )
