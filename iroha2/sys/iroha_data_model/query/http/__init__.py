
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
PaginatedQueryResult = make_struct("PaginatedQueryResult", [("result", "iroha_data_model.query.http.QueryResult"), ("filter", "iroha_data_model.predicate.GenericPredicateBox"), ("pagination", "iroha_data_model.pagination.Pagination"), ("sorting", "iroha_data_model.sorting.Sorting"), ("total", int)])

Payload = make_struct("Payload", [("timestamp_ms", "Compact"), ("query", "iroha_data_model.query.QueryBox"), ("account_id", "iroha_data_model.account.Id"), ("filter", "iroha_data_model.predicate.GenericPredicateBox")])

QueryResult = make_tuple("QueryResult", ["iroha_data_model.Value"])
SignedQueryRequest = make_struct("SignedQueryRequest", [("payload", "iroha_data_model.query.http.Payload"), ("signature", "iroha_crypto.signature.SignatureOf")])

VersionedPaginatedQueryResult = make_enum("VersionedPaginatedQueryResult", [("V1", get_class("iroha_data_model.query.http.PaginatedQueryResult"))], typing.Union[get_class("iroha_data_model.query.http.PaginatedQueryResult")])

VersionedSignedQueryRequest = make_enum("VersionedSignedQueryRequest", [("V1", get_class("iroha_data_model.query.http.SignedQueryRequest"))], typing.Union[get_class("iroha_data_model.query.http.SignedQueryRequest")])

SelfResolvingTypeVar.resolve_all()
