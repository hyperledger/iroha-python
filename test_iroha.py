import iroha


PRIVATE_KEY = b"aFJfbcedA7p6X0b6EdQNovfFtmq4YSGK/+Bw+XBrsnAEBpXRu+Qfw0559lgLwF2QusChGiDEkLAxPqodQH1kbA=="
PUBLIC_KEY = b"N1X+Fv7soLknpZNtkdW5cRphgzFjqHmOJl9GvVahWxk="
KEY_PAIR = iroha.KeyPair(private_key=PRIVATE_KEY, public_key=PUBLIC_KEY)


def test_sign_verify():
    message = b'test'
    signature = iroha.sign(KEY_PAIR, message)
    assert iroha.verify(KEY_PAIR.public_key, signature, message)
