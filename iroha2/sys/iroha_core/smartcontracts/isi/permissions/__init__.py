from .....rust import Enum, Struct, Tuple, Dict
ValidatorType = Enum[("Instruction", type(None)), ("Query", type(None)), ("Expression", type(None))] 
