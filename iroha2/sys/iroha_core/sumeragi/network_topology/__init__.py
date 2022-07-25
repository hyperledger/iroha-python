from ....rust import Enum, make_struct, make_tuple, Dict
Topology = make_struct("Topology", [("sorted_peers", list), ("at_block", "iroha_crypto.hash.HashOf"), ("view_change_proofs", "iroha_core.sumeragi.view_change.ProofChain")])

