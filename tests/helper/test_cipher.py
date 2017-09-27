from src.helper import crypto
import sha3
import unittest

class CipherTest(unittest.TestCase):
    def test_sha3_sign(self):
        key_pair = crypto.create_key_pair()
        message = crypto.sha3_256(bytes(b'a031b'))
        dummy_message = crypto.sha3_256(bytes(b'a032b'))
        sign = crypto.sign(key_pair,message)
        self.assertTrue(crypto.verify(key_pair.public_key,sign,message))
        self.assertFalse(crypto.verify(key_pair.public_key,sign,dummy_message))

    # verify sha3 URL : https://emn178.github.io/online-tools/sha3_256.html
    def test_trust_sha3(self):
        message = sha3.sha3_256(b'').hexdigest()
        self.assertEqual(message,'a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a')
        message = sha3.sha3_256(b'AmagaiRihito').hexdigest()
        self.assertEqual(message,'2fe9b3cbff5a2fb410564df7664c283d52c0f3a3cf6cb340568d95fe5353b7bb')
        message = sha3.sha3_256(b'YamadaYamato').hexdigest()
        self.assertEqual(message,'609b0336d8de8f8c807fdc3fc06d907f55cc838be039080680bc3b321ed06c5e')
        message = sha3.sha3_256(b'RindoShian').hexdigest()
        self.assertEqual(message,'4deda7d88607133ae34d0fcab00af0893087a10201890fe6751342be24f903d6')
        message = sha3.sha3_256(b'SportingSalt').hexdigest()
        self.assertEqual(message,'e44a1c8b9c9791e323f79eb465112280d7ba7c4b8000535812c910ef15b1cc81')
        message = sha3.sha3_256(b'He is a blue player.').hexdigest()
        self.assertEqual(message,'956c8b77a3f75aef6c0eaf5eee8cd1cdf132897842b8608b9b4f61b354d00f47')

