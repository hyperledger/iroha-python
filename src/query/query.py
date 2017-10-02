from schema.response_pb2 import Query as QuerySchema

from src.helper import logger, crypto, stateless_validator
from src.primitive.signatories import Signatories
from src.query.request import wrap_query

class Query:
    """
    class Query ; wrap of create query, sign, connevtin and response.
    """
    def __init__(self):
        logger.debug("Create Query Construct")
        self.query = QuerySchema(
            payload = QuerySchema.Payload(
                created_time = crypto.now()
            )
            # TODO query has signature
        )
        self.signatories = Signatories()


    def set_creator_account_id(self,creator_account_id):
        """
        Set creator of this query.

        :param creator_account_id: it is creator's account id of query
        """
        logger.debug("Query.set_creator_account_id")
        self.query.payload.creator_account_id = creator_account_id

    def set_query_counter(self,query_counter):
        """
        Set query counter of this query

        :param query_counter:
            query_counter is counter of query
        """
        logger.debug("Query.set_tx_counter")
        self.query.payload.query_counter = query_counter

    def time_stamp(self):
        """
        Set current(call this function) time timestamp of this query
        """
        logger.debug("Query.time_stamp")
        self.query.payload.created_time = crypto.now()

    def hash(self):
        """
        Get hash of this query

        :return: hash of this query
        """
        logger.debug("Query.hash")
        return crypto.sign_hash(self.query.payload)

    def verify(self):
        """
        Verify stateless validate this query

        :return:
            :True: stateless validation success
            :False: stateless validation failed
        """
        logger.debug("Query.verify")
        return stateless_validator.query(self.query)

    def set_request(self,request):
        """
        Set request strcuture of query

        :param request:
            It is request of query.
            `GetAccount`, `GetAccountTransactions`, `GetAccountAssetTransactions`, `GetTransactions`,
             `GetAccountAssets` or `GetSignatories`.
        """
        logger.debug("Query.set_request")
        wrap_query(self.query.payload,request)

    def debug_proto_query(self):
        """
        Debug function.
        Return query proto structure had this query.

        :return: Query protobuf data
        """
        logger.debug("debug_proto_query")
        return self.query

    def issue(self):
        """
        Issue to iroha for this query and return that response.

        :return: `Response` type ( this is wrapped QueryResponse proto structure )
            response from iroha respond to this query.
        """
        logger.debug("Query.issue")
        # TODO
