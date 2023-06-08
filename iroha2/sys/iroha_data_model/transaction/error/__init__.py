
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
InstructionExecutionFail = make_struct("InstructionExecutionFail", [("instruction", "iroha_data_model.isi.Instruction"), ("reason", str)])

NotPermittedFail = make_struct("NotPermittedFail", [("reason", str)])

TransactionExpired = make_struct("TransactionExpired", [("time_to_live_ms", int)])

TransactionLimitError = make_struct("TransactionLimitError", [("reason", str)])

TransactionRejectionReason = make_enum("TransactionRejectionReason", [("LimitCheck", get_class("iroha_data_model.transaction.error.TransactionLimitError")), ("NotPermitted", get_class("iroha_data_model.transaction.error.NotPermittedFail")), ("UnsatisfiedSignatureCondition", get_class("iroha_data_model.transaction.error.UnsatisfiedSignatureConditionFail")), ("InstructionExecution", get_class("iroha_data_model.transaction.error.InstructionExecutionFail")), ("WasmExecution", get_class("iroha_data_model.transaction.error.WasmExecutionFail")), ("UnexpectedGenesisAccountSignature", get_class(type(None))), ("Expired", get_class("iroha_data_model.transaction.error.TransactionExpired"))], typing.Union[get_class("iroha_data_model.transaction.error.TransactionLimitError"), get_class("iroha_data_model.transaction.error.NotPermittedFail"), get_class("iroha_data_model.transaction.error.UnsatisfiedSignatureConditionFail"), get_class("iroha_data_model.transaction.error.InstructionExecutionFail"), get_class("iroha_data_model.transaction.error.WasmExecutionFail"), get_class(type(None)), get_class("iroha_data_model.transaction.error.TransactionExpired")])

UnsatisfiedSignatureConditionFail = make_struct("UnsatisfiedSignatureConditionFail", [("reason", str)])

WasmExecutionFail = make_struct("WasmExecutionFail", [("reason", str)])

SelfResolvingTypeVar.resolve_all()
