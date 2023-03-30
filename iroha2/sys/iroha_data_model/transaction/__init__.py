
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Executable = make_enum("Executable", [("Instructions", get_class(list)), ("Wasm", get_class("iroha_data_model.transaction.WasmSmartContract"))], typing.Union[get_class(list), get_class("iroha_data_model.transaction.WasmSmartContract")])

Payload = make_struct("Payload", [("account_id", "iroha_data_model.account.Id"), ("instructions", "iroha_data_model.transaction.Executable"), ("creation_time", int), ("time_to_live_ms", int), ("nonce", int), ("metadata", Dict)])

RejectedTransaction = make_struct("RejectedTransaction", [("payload", "iroha_data_model.transaction.Payload"), ("signatures", "iroha_crypto.signature.SignaturesOf"), ("rejection_reason", "iroha_data_model.transaction.error.TransactionRejectionReason")])

SignedTransaction = make_struct("SignedTransaction", [("payload", "iroha_data_model.transaction.Payload"), ("signatures", list)])

TransactionLimits = make_struct("TransactionLimits", [("max_instruction_number", int), ("max_wasm_size_bytes", int)])

TransactionQueryResult = make_struct("TransactionQueryResult", [("tx_value", "iroha_data_model.transaction.TransactionValue"), ("block_hash", "iroha_crypto.hash.Hash")])

TransactionValue = make_enum("TransactionValue", [("Transaction", get_class("iroha_data_model.transaction.VersionedSignedTransaction")), ("RejectedTransaction", get_class("iroha_data_model.transaction.VersionedRejectedTransaction"))], typing.Union[get_class("iroha_data_model.transaction.VersionedSignedTransaction"), get_class("iroha_data_model.transaction.VersionedRejectedTransaction")])

ValidTransaction = make_struct("ValidTransaction", [("payload", "iroha_data_model.transaction.Payload"), ("signatures", "iroha_crypto.signature.SignaturesOf")])

VersionedRejectedTransaction = make_enum("VersionedRejectedTransaction", [("V1", get_class("iroha_data_model.transaction.RejectedTransaction"))], typing.Union[get_class("iroha_data_model.transaction.RejectedTransaction")])

VersionedSignedTransaction = make_enum("VersionedSignedTransaction", [("V1", get_class("iroha_data_model.transaction.SignedTransaction"))], typing.Union[get_class("iroha_data_model.transaction.SignedTransaction")])

VersionedValidTransaction = make_enum("VersionedValidTransaction", [("V1", get_class("iroha_data_model.transaction.ValidTransaction"))], typing.Union[get_class("iroha_data_model.transaction.ValidTransaction")])

WasmSmartContract = make_tuple("WasmSmartContract", [list])
SelfResolvingTypeVar.resolve_all()
