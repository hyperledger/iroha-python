from ...rust import Enum, make_struct, make_tuple, Dict
BlockRejectionReason = Enum[("ConsensusBlockRejection", type(None))] 
Executable = Enum[("Instructions", list), ("Wasm", "iroha_data_model.transaction.WasmSmartContract")] 
InstructionExecutionFail = make_struct("InstructionExecutionFail", [("instruction", "iroha_data_model.isi.Instruction"), ("reason", str)])

NotPermittedFail = make_struct("NotPermittedFail", [("reason", str)])

Payload = make_struct("Payload", [("account_id", "iroha_data_model.account.Id"), ("instructions", "iroha_data_model.transaction.Executable"), ("creation_time", int), ("time_to_live_ms", int), ("nonce", int), ("metadata", Dict)])

RejectedTransaction = make_struct("RejectedTransaction", [("payload", "iroha_data_model.transaction.Payload"), ("signatures", "iroha_crypto.signature.SignaturesOf"), ("rejection_reason", "iroha_data_model.transaction.TransactionRejectionReason")])

RejectionReason = Enum[("Block", "iroha_data_model.transaction.BlockRejectionReason"), ("Transaction", "iroha_data_model.transaction.TransactionRejectionReason")] 
Transaction = make_struct("Transaction", [("payload", "iroha_data_model.transaction.Payload"), ("signatures", list)])

TransactionLimitError = make_tuple("TransactionLimitError", [str])
TransactionQueryResult = make_struct("TransactionQueryResult", [("tx_value", "iroha_data_model.transaction.TransactionValue"), ("block_hash", "iroha_crypto.hash.Hash")])

TransactionRejectionReason = Enum[("NotPermitted", "iroha_data_model.transaction.NotPermittedFail"), ("UnsatisfiedSignatureCondition", "iroha_data_model.transaction.UnsatisfiedSignatureConditionFail"), ("LimitCheck", "iroha_data_model.transaction.TransactionLimitError"), ("InstructionExecution", "iroha_data_model.transaction.InstructionExecutionFail"), ("WasmExecution", "iroha_data_model.transaction.WasmExecutionFail"), ("UnexpectedGenesisAccountSignature", type(None))] 
TransactionValue = Enum[("Transaction", "iroha_data_model.transaction.VersionedTransaction"), ("RejectedTransaction", "iroha_data_model.transaction.VersionedRejectedTransaction")] 
UnsatisfiedSignatureConditionFail = make_struct("UnsatisfiedSignatureConditionFail", [("reason", str)])

ValidTransaction = make_struct("ValidTransaction", [("payload", "iroha_data_model.transaction.Payload"), ("signatures", "iroha_crypto.signature.SignaturesOf")])

VersionedRejectedTransaction = Enum[("V1", "iroha_data_model.transaction.RejectedTransaction")] 
VersionedTransaction = Enum[("V1", "iroha_data_model.transaction.Transaction")] 
VersionedValidTransaction = Enum[("V1", "iroha_data_model.transaction.ValidTransaction")] 
WasmExecutionFail = make_struct("WasmExecutionFail", [("reason", str)])

WasmSmartContract = make_struct("WasmSmartContract", [("raw_data", list)])

