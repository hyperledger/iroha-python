import unittest

from src.helper import logger,crypto
from src.query.query import Query, QuerySchema

from schema.response_pb2 import GetAccount, GetAccountAssets, GetTransactions

class QueryTest(unittest.TestCase):
    def setUp(self):
        logger.setDebug()
        logger.debug("QueryTest")

    def test_transaction(self):
        logger.debug("test_query")
        query = Query()
        query.set_creator_account_id("sioya@sporting.salt")
        query.time_stamp()

        query.set_request(
            GetAccount(account_id = "sioya@sporting.salt")
        )
        self.assertTrue(query.verify())
        qry = query.debug_proto_query()
        self.assertEqual(
            qry.payload,
            QuerySchema.Payload(
                creator_account_id = "sioya@sporting.salt",
                created_time = qry.payload.created_time,
                get_account = GetAccount(
                    account_id = "sioya@sporting.salt"
                )
            )
        )

        # overwrite
        query.set_request(
            GetAccountAssets(
                account_id = "sioya@sporting.salt",
                asset_id = "sporting.salt/zokin"
            )
        )
        self.assertTrue(query.verify())
        qry = query.debug_proto_query()
        self.assertEqual(
            qry.payload,
            QuerySchema.Payload(
                creator_account_id = "sioya@sporting.salt",
                created_time = qry.payload.created_time,
                get_account_assets = GetAccountAssets(
                account_id = "sioya@sporting.salt",
                asset_id = "sporting.salt/zokin"
                )
            )
        )

        query.set_request(
            GetTransactions(
                tx_hashes = [b"xx",b"aa"]
            )
        )
        self.assertFalse(query.verify())
