
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
BlockRejectionReason = make_enum("BlockRejectionReason", [("ConsensusBlockRejection", get_class(type(None)))], typing.Union[get_class(type(None))])

Executable = make_enum("Executable", [("Instructions", get_class(list)), ("Wasm", get_class("iroha_data_model.transaction.WasmSmartContract"))], typing.Union[get_class(list), get_class("iroha_data_model.transaction.WasmSmartContract")])

InstructionExecutionFail = make_struct("InstructionExecutionFail", [("instruction", "iroha_data_model.isi.Instruction"), ("reason", str)])

NotPermittedFail = make_struct("NotPermittedFail", [("reason", str)])

Payload = make_struct("Payload", [("account_id", "iroha_data_model.account.Id"), ("instructions", "iroha_data_model.transaction.Executable"), ("creation_time", int), ("time_to_live_ms", int), ("nonce", int), ("metadata", Dict)])

RejectedTransaction = make_struct("RejectedTransaction", [("payload", "iroha_data_model.transaction.Payload"), ("signatures", "iroha_crypto.signature.SignaturesOf"), ("rejection_reason", "iroha_data_model.transaction.TransactionRejectionReason")])

RejectionReason = make_enum("RejectionReason", [("Block", get_class("iroha_data_model.transaction.BlockRejectionReason")), ("Transaction", get_class("iroha_data_model.transaction.TransactionRejectionReason"))], typing.Union[get_class("iroha_data_model.transaction.BlockRejectionReason"), get_class("iroha_data_model.transaction.TransactionRejectionReason")])

SignedTransaction = make_struct("SignedTransaction", [("payload", "iroha_data_model.transaction.Payload"), ("signatures", list)])

TransactionLimitError = make_tuple("TransactionLimitError", [str])
TransactionQueryResult = make_struct("TransactionQueryResult", [("tx_value", "iroha_data_model.transaction.TransactionValue"), ("block_hash", "iroha_crypto.hash.Hash")])

TransactionRejectionReason = make_enum("TransactionRejectionReason", [("NotPermitted", get_class("iroha_data_model.transaction.NotPermittedFail")), ("UnsatisfiedSignatureCondition", get_class("iroha_data_model.transaction.UnsatisfiedSignatureConditionFail")), ("LimitCheck", get_class("iroha_data_model.transaction.TransactionLimitError")), ("InstructionExecution", get_class("iroha_data_model.transaction.InstructionExecutionFail")), ("WasmExecution", get_class("iroha_data_model.transaction.WasmExecutionFail")), ("UnexpectedGenesisAccountSignature", get_class(type(None)))], typing.Union[get_class("iroha_data_model.transaction.NotPermittedFail"), get_class("iroha_data_model.transaction.UnsatisfiedSignatureConditionFail"), get_class("iroha_data_model.transaction.TransactionLimitError"), get_class("iroha_data_model.transaction.InstructionExecutionFail"), get_class("iroha_data_model.transaction.WasmExecutionFail"), get_class(type(None))])

TransactionValue = make_enum("TransactionValue", [("Transaction", get_class("iroha_data_model.transaction.VersionedSignedTransaction")), ("RejectedTransaction", get_class("iroha_data_model.transaction.VersionedRejectedTransaction"))], typing.Union[get_class("iroha_data_model.transaction.VersionedSignedTransaction"), get_class("iroha_data_model.transaction.VersionedRejectedTransaction")])

UnsatisfiedSignatureConditionFail = make_struct("UnsatisfiedSignatureConditionFail", [("reason", str)])

ValidTransaction = make_struct("ValidTransaction", [("payload", "iroha_data_model.transaction.Payload"), ("signatures", "iroha_crypto.signature.SignaturesOf")])

VersionedRejectedTransaction = make_enum("VersionedRejectedTransaction", [("V1", get_class("iroha_data_model.transaction.RejectedTransaction"))], typing.Union[get_class("iroha_data_model.transaction.RejectedTransaction")])

VersionedSignedTransaction = make_enum("VersionedSignedTransaction", [("V1", get_class("iroha_data_model.transaction.SignedTransaction"))], typing.Union[get_class("iroha_data_model.transaction.SignedTransaction")])

VersionedValidTransaction = make_enum("VersionedValidTransaction", [("V1", get_class("iroha_data_model.transaction.ValidTransaction"))], typing.Union[get_class("iroha_data_model.transaction.ValidTransaction")])

WasmExecutionFail = make_struct("WasmExecutionFail", [("reason", str)])

WasmSmartContract = make_struct("WasmSmartContract", [("raw_data", list)])

SelfResolvingTypeVar.resolve_all()
