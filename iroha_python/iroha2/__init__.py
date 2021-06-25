#!/usr/bin/env python
from .sys.rust import *
from .sys import KeyPair, Client as _Client


class Client:
    def __init__(self, cfg):
        self.cl = _Client(cfg)

    def submit_tx(self, tx: list):
        tx = [i.to_rust() for i in tx]
        return self.cl.submit_all_with_metadata(tx, {})

    def submit_inst(self, inst):
        return self.cl.submit_all_with_metadata([inst.to_rust()], {})
