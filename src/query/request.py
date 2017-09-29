from schema.response_pb2 import GetAccount, GetAccountTransactions, GetAccountAssetTransactions, GetTransactions, GetAccountAssets, GetSignatories
from src.helper import logger

def wrap_query(query_payload,request):
    if type(request) == type(GetAccount()):
        query_payload.get_account.CopyFrom(request)
    elif type(request) == type(GetSignatories()):
        query_payload.get_signatories.CopyFrom(request)
    elif type(request) == type(GetAccountAssets()):
        query_payload.get_account_assets.CopyFrom(request)
    elif type(request) == type(GetAccountTransactions()):
        query_payload.get_account_transactions.CopyFrom(request)
    elif type(request) == type(GetAccountAssetTransactions()):
        query_payload.get_account_asset_transactions.CopyFrom(request)
    elif type(request) == type(GetTransactions()):
        query_payload.get_transactions.CopyFrom(request)
    else:
        logger.warning("Request Not Match ReqeustType")
