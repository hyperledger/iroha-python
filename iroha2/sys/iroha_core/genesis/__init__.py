from ...rust import Enum, make_struct, make_tuple, Dict
GenesisTransaction = make_struct("GenesisTransaction", [("isi", list)])

RawGenesisBlock = make_struct("RawGenesisBlock", [("transactions", list)])

