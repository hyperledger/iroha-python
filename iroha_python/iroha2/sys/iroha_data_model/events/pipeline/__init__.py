from ....rust import Enum, Struct, Tuple, Dict

EntityType = Enum[("Block", type(None)), ("Transaction", type(None))]
EventFilter = Struct[("entity", "iroha_data_model.events.pipeline.EntityType"),
                     ("hash", "iroha_crypto.Hash")]

InstructionExecutionFail = Struct[("instruction",
                                   "iroha_data_model.isi.Instruction"),
                                  ("reason", str)]

NotPermittedFail = Struct[("reason", str)]

SignatureVerificationFail = Struct[("signature", "iroha_crypto.Signature"),
                                   ("reason", str)]

TransactionRejectionReason = Enum[
    ("NotPermitted", "iroha_data_model.events.pipeline.NotPermittedFail"),
    ("UnsatisfiedSignatureCondition",
     "iroha_data_model.events.pipeline.UnsatisfiedSignatureConditionFail"),
    ("InstructionExecution",
     "iroha_data_model.events.pipeline.InstructionExecutionFail"),
    ("SignatureVerification",
     "iroha_data_model.events.pipeline.SignatureVerificationFail"),
    ("UnexpectedGenesisAccountSignature", type(None))]
UnsatisfiedSignatureConditionFail = Struct[("reason", str)]
