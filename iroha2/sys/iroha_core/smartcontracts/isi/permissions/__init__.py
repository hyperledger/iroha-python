from .....rust import Enum, make_struct, make_tuple, Dict
ValidatorType = Enum[("Instruction", type(None)), ("Query", type(None)), ("Expression", type(None))] 
