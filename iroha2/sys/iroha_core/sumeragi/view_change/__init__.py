
from ....rust import make_enum, make_struct, make_tuple, Dict, get_class
import typing
            
BlockCreationTimeout = make_tuple("BlockCreationTimeout")
CommitTimeout = make_struct("CommitTimeout", [("hash", "iroha_crypto.hash.HashOf")])

NoTransactionReceiptReceived = make_tuple("NoTransactionReceiptReceived")
Proof = make_struct("Proof", [("payload", "iroha_core.sumeragi.view_change.ProofPayload"), ("signatures", "iroha_crypto.signature.SignaturesOf")])

ProofChain = make_struct("ProofChain", [("proofs", list)])

ProofPayload = make_struct("ProofPayload", [("previous_proof", "iroha_crypto.hash.HashOf"), ("latest_block", "iroha_crypto.hash.HashOf"), ("reason", "iroha_core.sumeragi.view_change.Reason")])

Reason = make_enum("Reason", [("CommitTimeout", get_class("iroha_core.sumeragi.view_change.CommitTimeout")), ("NoTransactionReceiptReceived", get_class("iroha_core.sumeragi.view_change.NoTransactionReceiptReceived")), ("BlockCreationTimeout", get_class("iroha_core.sumeragi.view_change.BlockCreationTimeout"))], typing.Union[get_class("iroha_core.sumeragi.view_change.CommitTimeout"), get_class("iroha_core.sumeragi.view_change.NoTransactionReceiptReceived"), get_class("iroha_core.sumeragi.view_change.BlockCreationTimeout")])
