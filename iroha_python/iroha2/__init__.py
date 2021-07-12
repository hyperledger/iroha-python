#!/usr/bin/env python
from .sys.rust import *
from .sys import KeyPair, Client as _Client
from .data_model.query import Query as _Query



class Client:
    def __init__(self, cfg):
        self.cl = _Client(cfg)

    @property
    def account(self):
        return self.cl.account

    def submit_tx(self, tx: list):
        tx = [i.to_rust() for i in tx]
        return self.cl.submit_all_with_metadata(tx, {})

    def submit_isi(self, isi):
        return self.submit_tx([isi])

    def submit_tx_blocking(self, tx: list):
        tx = [i.to_rust() for i in tx]
        return self.cl.submit_all_blocking_with_metadata(tx, {})

    def submit_isi_blocking(self, isi):
        return self.submit_tx_blocking([isi])

    def query(self, query):
        return self.cl.request(_Query(query))

    def listen(self, events_kind):
        return self.cl.listen_for_events(events_kind)
