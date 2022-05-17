from ....rust import Enum, Struct, Tuple, Dict
BlockCreationTimeout = Tuple[()]
CommitTimeout = Struct[("hash", "iroha_crypto.hash.HashOf")]

NoTransactionReceiptReceived = Tuple[()]
Proof = Struct[("payload", "iroha_core.sumeragi.view_change.ProofPayload"), ("signatures", "iroha_crypto.signature.SignaturesOf")]

ProofChain = Struct[("proofs", list)]

ProofPayload = Struct[("previous_proof", "iroha_crypto.hash.HashOf"), ("latest_block", "iroha_crypto.hash.HashOf"), ("reason", "iroha_core.sumeragi.view_change.Reason")]

Reason = Enum[("CommitTimeout", "iroha_core.sumeragi.view_change.CommitTimeout"), ("NoTransactionReceiptReceived", "iroha_core.sumeragi.view_change.NoTransactionReceiptReceived"), ("BlockCreationTimeout", "iroha_core.sumeragi.view_change.BlockCreationTimeout")] 
