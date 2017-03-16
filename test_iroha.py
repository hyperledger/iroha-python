import codecs
import io

import flatbuffers

import iroha
import _generated.iroha.BaseObject as base_object
import _generated.iroha.BaseObjectType as base_object_type


def test_create_key_pair():
    zeros32 = codecs.decode('00' * 32, 'hex')
    keypair = iroha.create_key_pair(zeros32)
    assert len(keypair.private_key) == 64
    assert len(keypair.public_key) == 32


def test_sign_verify():
    zeros32 = codecs.decode('00' * 32, 'hex')
    keypair = iroha.create_key_pair(zeros32)
    msg = b'test'
    signature = iroha.sign(keypair, msg)
    assert iroha.verify(keypair.public_key, signature, msg)


def test_sha3_256():
    h = 'a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a'
    assert iroha.sha3_256(b'') == codecs.decode(h, 'hex')


def test_sha3_384():
    h = ('0c63a75b845e4f7d01107d852e4c2485c51a50aaaa94fc61'
         '995e71bbee983a2ac3713831264adb47fb6bd1e058d5f004')
    assert iroha.sha3_384(b'') == codecs.decode(h, 'hex')


def test_sha3_512():
    h = ('a69f73cca23a9ac5c8b567dc185a756e97c982164fe25859e0d1dcc1475c80a6'
         '15b2123af1f5f94c11e3e9402c3ac558f500199d95b6d3e301758586281dcd26')
    assert iroha.sha3_512(b'') == codecs.decode(h, 'hex')


def test_flatbuffers_base_object():
    # Build the byte buffer.
    b = flatbuffers.Builder(0)
    name = b.CreateString('treasure')
    base_object.BaseObjectStart(b)
    base_object.BaseObjectAddName(b, name)
    base_object.BaseObjectAddType(b, base_object_type.BaseObjectType.Integer)
    base_object.BaseObjectAddInteger(b, 7777777)
    baseobjptr = base_object.BaseObjectEnd(b)
    b.Finish(baseobjptr)
    baseobjbytes = b.Output()

    # Read the object from the byte buffer.
    f = io.BytesIO(baseobjbytes)
    buf = f.read()
    obj = base_object.BaseObject.GetRootAsBaseObject(buf, 0)

    # Object values should be equal to the written ones.
    assert obj.Name() == b'treasure'
    assert obj.Type() == base_object_type.BaseObjectType.Integer
    assert obj.Integer() == 7777777
