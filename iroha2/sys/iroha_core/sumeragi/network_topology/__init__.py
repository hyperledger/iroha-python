from ....rust import Enum, Struct, Tuple, Dict
Topology = Struct[("sorted_peers", list), ("at_block", "iroha_crypto.hash.HashOf"), ("view_change_proofs", "iroha_core.sumeragi.view_change.ProofChain")]

