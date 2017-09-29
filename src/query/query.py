from schema.response_pb2 import Query as QuerySchema

from src.helper import logger, crypto, stateless_validator
from src.primitive.signatories import Signatories
from src.query.request import wrap_query

class Query:
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
        logger.debug("Query.set_creator_account_id")
        self.query.payload.creator_account_id = creator_account_id

    def set_query_counter(self,query_counter):
        logger.debug("Query.set_tx_counter")
        self.query.payload.query_counter = query_counter

    def time_stamp(self):
        logger.debug("Query.time_stamp")
        self.query.payload.created_time = crypto.now()

    def hash(self):
        logger.debug("Query.hash")
        return crypto.sign_hash(self.query.payload)

    def verify(self):
        logger.debug("Query.verify")
        return stateless_validator.query(self.query)

    def set_request(self,request):
        logger.debug("Query.set_request")
        wrap_query(self.query.payload,request)

    def debug_proto_query(self):
        logger.debug("debug_porto_query")
        return self.query

    def issue(self):
        logger.debug("Query.issue")
        # TODO
