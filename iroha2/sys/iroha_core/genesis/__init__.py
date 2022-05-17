from ...rust import Enum, Struct, Tuple, Dict
GenesisTransaction = Struct[("isi", list)]

RawGenesisBlock = Struct[("transactions", list)]

