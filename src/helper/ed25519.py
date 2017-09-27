from ctypes import *
import base64

libed2559 = cdll.LoadLibrary('./src/lib/ed25519/lib/libed25519.so')


def generate():
    seed = POINTER(c_ubyte)((c_ubyte * 32)())
    public_key = POINTER(c_ubyte)((c_ubyte * 32)())
    private_key = POINTER(c_ubyte)((c_ubyte * 64)())

    libed2559.ed25519_create_seed.argtypes = [POINTER(c_ubyte)]
    libed2559.ed25519_create_seed(seed)
    libed2559.ed25519_create_keypair.argtypes = [POINTER(c_ubyte), POINTER(c_ubyte), POINTER(c_ubyte)]
    libed2559.ed25519_create_keypair(public_key, private_key, seed)
    publist = []
    for i in range(32):
        publist.append(public_key[i])
    print(publist)
    publicKey64 = base64.b64encode(bytes(publist))

    prilist = []
    for i in range(64):
        prilist.append(private_key[i])
    print(prilist)
    privateKey64 = base64.b64encode(bytes(prilist))

    return (publicKey64, privateKey64)


def generate_int():
    seed = POINTER(c_ubyte)((c_ubyte * 32)())
    public_key = POINTER(c_ubyte)((c_ubyte * 32)())
    private_key = POINTER(c_ubyte)((c_ubyte * 64)())

    libed2559.ed25519_create_seed.argtypes = [POINTER(c_ubyte)]
    libed2559.ed25519_create_seed(seed)
    libed2559.ed25519_create_keypair.argtypes = [POINTER(c_ubyte), POINTER(c_ubyte), POINTER(c_ubyte)]
    libed2559.ed25519_create_keypair(public_key, private_key, seed)
    publist = []
    for i in range(32):
        publist.append(public_key[i])

    prilist = []
    for i in range(64):
        prilist.append(private_key[i])

    return (publist, prilist)

"""
ed25519_sign(
  unsigned char *signature,
  const unsigned char *message,
  size_t message_len,
  const unsigned char *public_key,
  const unsigned char *private_key
);
"""


def sign(message, public, private):
    signature = POINTER(c_ubyte)((c_ubyte * 64)())
    libed2559.ed25519_sign.argtypes = [POINTER(c_ubyte), POINTER(c_ubyte), c_long, POINTER(c_ubyte), POINTER(c_ubyte)]
    libed2559.ed25519_sign(
        signature,
        POINTER(c_ubyte)((c_ubyte * len(message)).from_buffer_copy(message)),
        len(message),
        POINTER(c_ubyte)((c_ubyte * len(base64.b64decode(public))).from_buffer_copy(base64.b64decode(public))),
        POINTER(c_ubyte)((c_ubyte * len(base64.b64decode(private))).from_buffer_copy(base64.b64decode(private)))
    )

    siglist = []
    for i in range(64):
        siglist.append(signature[i])
    print(len(siglist))
    return base64.b64encode(bytes(siglist))


def sign_int(message, public, private):
    signature = POINTER(c_ubyte)((c_ubyte * 64)())
    libed2559.ed25519_sign.argtypes = [POINTER(c_ubyte), POINTER(c_ubyte), c_long, POINTER(c_ubyte), POINTER(c_ubyte)]
    libed2559.ed25519_sign(
        signature,
        POINTER(c_ubyte)((c_ubyte * len(message)).from_buffer_copy(message)),
        len(message),
        POINTER(c_ubyte)((c_ubyte * len(public)).from_buffer_copy(bytes(public))),
        POINTER(c_ubyte)((c_ubyte * len(private)).from_buffer_copy(bytes(private)))
    )
    siglist = []
    for i in range(64):
        siglist.append(signature[i])
    return siglist


def verify_int(message, signature, public):
    libed2559.ed25519_verify.argtypes = [POINTER(c_ubyte), POINTER(c_ubyte), c_long, POINTER(c_ubyte)]
    print('int sig:', signature)
    print('int siglen:', len(signature))
    print('int pub:', public)
    print('int publen:', len(public))
    return libed2559.ed25519_verify(
        POINTER(c_ubyte)((c_ubyte * len(signature)).from_buffer_copy(bytes(signature))),
        POINTER(c_ubyte)((c_ubyte * len(message)).from_buffer_copy(message)),
        len(message),
        POINTER(c_ubyte)((c_ubyte * len(public)).from_buffer_copy(bytes(public))),
    )


"""
ed25519_verify(
  const unsigned char *signature,
  const unsigned char *message,
  size_t message_len,
  const unsigned char *public_key
);
"""


def verify(message, signature, public):
    libed2559.ed25519_verify.argtypes = [POINTER(c_ubyte), POINTER(c_ubyte), c_long, POINTER(c_ubyte)]
    return libed2559.ed25519_verify(
        POINTER(c_ubyte)((c_ubyte * len(base64.b64decode(signature))).from_buffer_copy(base64.b64decode(signature))),
        POINTER(c_ubyte)((c_ubyte * len(message)).from_buffer_copy(message)),
        len(message),
        POINTER(c_ubyte)((c_ubyte * len(base64.b64decode(public))).from_buffer_copy(base64.b64decode(public))),
    )


def hex2bin(message):
    b = []
    for i in range(len(message) - 1):
        b.append(int(
            '0b' + format(int(chr(message[i]), 16), 'b').zfill(4) + format(int(chr(message[i + 1]), 16), 'b').zfill(4),
            2))
    return b[::2]


def verify_with_hex(message, signature, public):
    print(hex2bin(public))

    pubhex = b''.join(list(map(lambda x: x.to_bytes(1, byteorder='big'), hex2bin(public))))
    sighex = b''.join(list(map(lambda x: x.to_bytes(1, byteorder='big'), hex2bin(signature))))

    libed2559.ed25519_verify.argtypes = [POINTER(c_ubyte), POINTER(c_ubyte), c_long, POINTER(c_ubyte)]
    return libed2559.ed25519_verify(
        POINTER(c_ubyte)((c_ubyte * 64).from_buffer_copy(sighex)),
        POINTER(c_ubyte)((c_ubyte * 64).from_buffer_copy(message)),
        len(message),
        POINTER(c_ubyte)((c_ubyte * 32).from_buffer_copy(pubhex)),
    )

