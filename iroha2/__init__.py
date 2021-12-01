#!/usr/bin/env python
from .sys.rust import *
from .sys import KeyPair, Client as _Client
from .data_model.query import Query as _Query
from .data_model.isi import Instruction as _Instruction


class Client:
    def __init__(self, cfg):
        self.cl = _Client(cfg)

    @property
    def account(self):
        return self.cl.account

    @account.setter
    def account(self, account):
        self.cl.account = account

    @property
    def headers(self):
        return self.cl.headers

    @headers.setter
    def headers(self, headers):
        self.cl.headers = headers

    def tx_body(self, tx: list):
        return self.cl.tx_body(tx, {})

    def query_body(self, query):
        return self.cl.query_body(_Query(query))

    def submit_tx(self, tx: list):
        tx = [i.to_rust() for i in tx]
        return self.cl.submit_all_with_metadata(tx, {})

    def submit_isi(self, isi):
        return self.submit_tx([_Instruction(isi)])

    def submit_tx_blocking(self, tx: list):
        tx = [i.to_rust() for i in tx]
        return self.cl.submit_all_blocking_with_metadata(tx, {})

    def submit_isi_blocking(self, isi):
        return self.submit_tx_blocking([_Instruction(isi)])

    def query(self, q):
        out = self.cl.request(_Query(q))
        return q.parse_output(out) if hasattr(q, "parse_output") else out

    def listen(self, events_kind):
        return self.cl.listen_for_events(events_kind)
