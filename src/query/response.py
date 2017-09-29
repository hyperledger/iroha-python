from src.helper import logger, crypto
from src.helper.exception import NotErrorResponseException, NotAccountAssetResponseException, NotAccountResponseException, NotSignatoriesResponseExcepiton, NotTransactionsResponseException

class Response:
    def __init__(self,query_response):
        logger.info("Create Response Construct")
        self.response = query_response

    def verify(self):
        logger.debug("Response.verify")
        return crypto.verify(
            self.response.signature.pubkey,
            self.response.signature.signature,
            crypto.sign_hash(self.response.payload)
        )

    def has_account(self):
        logger.debug("Response.has_account")
        return self.response.HasField("account_response")

    def account(self):
        logger.debug("Response.account_response")
        if self.has_account():
            return self.response.account_response.account
        else:
            raise NotAccountResponseException

    def has_account_asset(self):
        logger.debug("Response.has_account_asset")
        return self.response.HasField("account_assets_response")

    def account_asset(self):
        logger.debug("Response.account_asset")
        if self.has_account_asset():
            return self.response.account_assets_response.account_asset
        else:
            raise NotAccountAssetResponseException

    def has_signatories(self):
        logger.debug("Response.has_signatories")
        return self.response.HasField("signatories_response")

    def signatories(self):
        logger.debug("Response.signatories")
        if self.has_signatories():
            return self.response.signatories_response.keys
        else:
            raise NotSignatoriesResponseExcepiton

    def has_transactions(self):
        logger.debug("Response.has_transactions")
        return self.response.HasField("transactions_response")

    def transactions(self):
        logger.debug("Response.transactions")
        if self.has_transactions():
            return self.response.transactions_response.transactions
        else:
            raise NotTransactionsResponseException

    def has_error(self):
        logger.debug("Response.has_error")
        return self.response.HasField("error_response")

    def error_response(self):
        logger.debug("Response.error_response")
        if self.has_error():
            return self.response.error_response
        else:
            raise NotErrorResponseException
