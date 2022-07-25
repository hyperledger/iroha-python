from ....rust import Enum, make_struct, make_tuple, Dict
BlockCreationTimeout = make_tuple("BlockCreationTimeout")
CommitTimeout = make_struct("CommitTimeout", [("hash", "iroha_crypto.hash.HashOf")])

NoTransactionReceiptReceived = make_tuple("NoTransactionReceiptReceived")
Proof = make_struct("Proof", [("payload", "iroha_core.sumeragi.view_change.ProofPayload"), ("signatures", "iroha_crypto.signature.SignaturesOf")])

ProofChain = make_struct("ProofChain", [("proofs", list)])

ProofPayload = make_struct("ProofPayload", [("previous_proof", "iroha_crypto.hash.HashOf"), ("latest_block", "iroha_crypto.hash.HashOf"), ("reason", "iroha_core.sumeragi.view_change.Reason")])

Reason = Enum[("CommitTimeout", "iroha_core.sumeragi.view_change.CommitTimeout"), ("NoTransactionReceiptReceived", "iroha_core.sumeragi.view_change.NoTransactionReceiptReceived"), ("BlockCreationTimeout", "iroha_core.sumeragi.view_change.BlockCreationTimeout")] 
