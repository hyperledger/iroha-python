from ...rust import Enum, Struct, Tuple, Dict
BlockRejectionReason = Enum[("ConsensusBlockRejection", type(None))] 
Executable = Enum[("Instructions", list), ("Wasm", "iroha_data_model.transaction.WasmSmartContract")] 
InstructionExecutionFail = Struct[("instruction", "iroha_data_model.isi.Instruction"), ("reason", str)]

NotPermittedFail = Struct[("reason", str)]

Payload = Struct[("account_id", "iroha_data_model.account.Id"), ("instructions", "iroha_data_model.transaction.Executable"), ("creation_time", int), ("time_to_live_ms", int), ("nonce", int), ("metadata", Dict)]

RejectedTransaction = Struct[("payload", "iroha_data_model.transaction.Payload"), ("signatures", "iroha_crypto.signature.SignaturesOf"), ("rejection_reason", "iroha_data_model.transaction.TransactionRejectionReason")]

RejectionReason = Enum[("Block", "iroha_data_model.transaction.BlockRejectionReason"), ("Transaction", "iroha_data_model.transaction.TransactionRejectionReason")] 
Transaction = Struct[("payload", "iroha_data_model.transaction.Payload"), ("signatures", list)]

TransactionLimitError = Tuple[str]
TransactionRejectionReason = Enum[("NotPermitted", "iroha_data_model.transaction.NotPermittedFail"), ("UnsatisfiedSignatureCondition", "iroha_data_model.transaction.UnsatisfiedSignatureConditionFail"), ("LimitCheck", "iroha_data_model.transaction.TransactionLimitError"), ("InstructionExecution", "iroha_data_model.transaction.InstructionExecutionFail"), ("WasmExecution", "iroha_data_model.transaction.WasmExecutionFail"), ("UnexpectedGenesisAccountSignature", type(None))] 
TransactionValue = Enum[("Transaction", "iroha_data_model.transaction.VersionedTransaction"), ("RejectedTransaction", "iroha_data_model.transaction.VersionedRejectedTransaction")] 
UnsatisfiedSignatureConditionFail = Struct[("reason", str)]

ValidTransaction = Struct[("payload", "iroha_data_model.transaction.Payload"), ("signatures", "iroha_crypto.signature.SignaturesOf")]

VersionedRejectedTransaction = Enum[("V1", "iroha_data_model.transaction.RejectedTransaction")] 
VersionedTransaction = Enum[("V1", "iroha_data_model.transaction.Transaction")] 
VersionedValidTransaction = Enum[("V1", "iroha_data_model.transaction.ValidTransaction")] 
WasmExecutionFail = Struct[("reason", str)]

WasmSmartContract = Struct[("raw_data", list)]

