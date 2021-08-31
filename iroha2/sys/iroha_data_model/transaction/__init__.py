from ...rust import Enum, Struct, Tuple, Dict

Payload = Struct[("account_id", "iroha_data_model.account.Id"),
                 ("instructions", list), ("creation_time", int),
                 ("time_to_live_ms", int), ("metadata", Dict)]

RejectedTransaction = Struct[(
    "payload", "iroha_data_model.transaction.Payload"), ("signatures", list), (
        "rejection_reason",
        "iroha_data_model.events.pipeline.TransactionRejectionReason")]

Transaction = Struct[("payload", "iroha_data_model.transaction.Payload"),
                     ("signatures", list)]

TransactionValue = Enum[(
    "Transaction", "iroha_data_model.transaction.VersionedTransaction"), (
        "RejectedTransaction",
        "iroha_data_model.transaction.VersionedRejectedTransaction")]
VersionedRejectedTransaction = Enum[(
    "V1", "iroha_data_model.transaction._VersionedRejectedTransactionV1")]
VersionedTransaction = Enum[(
    "V1", "iroha_data_model.transaction._VersionedTransactionV1")]
_VersionedRejectedTransactionV1 = Tuple[
    "iroha_data_model.transaction.RejectedTransaction"]
_VersionedTransactionV1 = Tuple["iroha_data_model.transaction.Transaction"]
