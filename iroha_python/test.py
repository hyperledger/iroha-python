#!/usr/bin/env python3
import iroha2
import json

from iroha2 import Client
from iroha2.data_model.isi import *
from iroha2.data_model.domain import *
from iroha2.data_model.expression import *
from iroha2.data_model import *

cfg = json.loads(open("./config.json").read())
cl = Client(cfg)

domain = Domain("xor")
register = Instruction(RegisterBox(Expression(Value(IdentifiableBox(domain)))))

cl.submit_inst(register)
