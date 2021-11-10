#!/usr/bin/env python3
from iroha2 import Dict, List


def test_list_iterable():
    assert [i for i in List(2, 3, 4)] == [2, 3, 4]


def test_dict_iterable():
    origin = {'a': 2, 'b': 3}
    d = Dict(**origin)

    assert set(i for i in d) == set(i for i in origin)
    assert set(i for i in d.items()) == set(i for i in origin.items())
    assert set(i for i in d.keys()) == set(i for i in origin.keys())
    assert set(i for i in d.values()) == set(i for i in origin.values())
