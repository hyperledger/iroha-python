from schema.response_pb2 import GetAccount, GetAccountTransactions, GetAccountAssetTransactions, GetTransactions, GetAccountAssets, GetSignatories, Query
from iroha.helper import logger
from iroha.query.request import wrap_query

import unittest


class RequestTest(unittest.TestCase):
    def setUp(self):
        logger.setInfo()
        logger.info("RequestTest")

    def test_request_get_account(self):
        logger.info("test_request_get_account")
        req = GetAccount(
            account_id = "test@test"
        )
        payload = Query.Payload()
        wrap_query(payload,req)
        self.assertEqual(payload,Query.Payload(
            get_account = req
        ))

    def test_request_get_account_asset(self):
        logger.info("test_request_get_account_asset")
        req = GetAccountAssets(
            account_id = "test@test",
            asset_id = "test/test"
        )
        payload = Query.Payload()
        wrap_query(payload,req)
        self.assertEqual(payload,Query.Payload(
            get_account_assets = req
        ))

    def test_request_get_signatories(self):
        logger.info("test_request_get_signatories")
        req = GetSignatories(
            account_id = "test@test"
        )
        payload = Query.Payload()
        wrap_query(payload,req)
        self.assertEqual(payload,Query.Payload(
            get_signatories = req
        ))


    def test_request_get_account_transactions(self):
        logger.info("test_request_get_account_transactions")
        req = GetAccountTransactions(
            account_id = "test@test"
        )
        payload = Query.Payload()
        wrap_query(payload,req)
        self.assertEqual(payload,Query.Payload(
            get_account_transactions = req
        ))


    def test_request_get_account_asset_transactions(self):
        logger.info("test_request_get_account_asset_transactions")
        req = GetAccountAssetTransactions(
            account_id = "test@test",
            asset_id = "test/test"
        )
        payload = Query.Payload()
        wrap_query(payload,req)
        self.assertEqual(payload,Query.Payload(
            get_account_asset_transactions = req
        ))


    def test_request_get_transactions(self):
        logger.info("test_request_get_transactions")
        req = GetTransactions(
            tx_hashes = []
        )
        payload = Query.Payload()
        wrap_query(payload,req)
        self.assertEqual(payload,Query.Payload(
            get_transactions = req
        ))

