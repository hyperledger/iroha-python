from iroha.helper import crypto, ed25519
import unittest

class Ed25519Test(unittest.TestCase):

    def test_ed25519(self):
        pubb, prib = ed25519.generate()

        private_key = b"+BTZfRSPRgDdxmjZlK+QhJ3RQryMH23LIPqg5C/Eu2QcBoj3QM6ovTcmPok0iFYI1y9M683ZS4Ifp10jr9dQrQ=="
        public_key = b"b+etgin9x1S16omALSjr4HTVzv9IEXQzlvSTp7el0Js="

        signature = b"HlJIjuds2OaSeyOjWjpnpXis55NvH3TD1SNVEwedu7sAY+Ypkksg3ovHUGfBhwd8uVmIX+JgnjrhKgPdyeO7DA=="
        message = b"0f1a39c82593e8b48e69f000c765c8e8072269d3bd4010634fa51d4e685076e30db22a9fb75def7379be0e808392922cb8c43d5dd5d5039828ed7ade7e1c6c81"

        signatureb = ed25519.sign(message, pubb, prib)

        print('b pygene pub: ', pubb)
        print('b pygene publen:', len(pubb))
        print('b pygene pro: ', prib)
        print('b pygen sig: ', signatureb)
        print('b pygen sig: ', len(signatureb))

        print(ed25519.verify(
            message,
            signatureb,
            pubb
        ))
        self.assertTrue(ed25519.verify(
            message,
            signatureb,
            pubb
        ))

        print('android verify is ', ed25519.verify(
            message,
            signature,
            public_key
        ))
        self.assertTrue(
            ed25519.verify(
                message,
                signature,
                public_key
            )
        )

        signature_android = ed25519.sign(message, public_key, private_key)

        print('android\'s key sign and verify is ', ed25519.verify(
            message,
            signature_android,
            public_key
        ))
        self.assertTrue(ed25519.verify(
            message,
            signature_android,
            public_key
        ))


    def test_crypt_ed25519(self):
        key_pair = crypto.create_key_pair()
        message = b"c0a5cca43b8aa79eb50e3464bc839dd6fd414fae0ddf928ca23dcebf8a8b8dd0"

        signature = crypto.sign(key_pair,message)
        sig_2 = ed25519.sign(message,key_pair.public_key,key_pair.private_key)
        self.assertEqual(signature,sig_2)

        self.assertTrue(crypto.verify(
            key_pair.public_key,
            signature,
            message
        ))

        go_pubkey = b"ZipcethJh6X7GCeYSPsD/FQLo5gbqcDU1S+yG8JKVJ0="
        # go_privkey = b"lP7Z+eyg91OEyS1T0QvZHk95eaoW5inOIhNLz/jRlUFmKlx62EmHpfsYJ5hI+wP8VAujmBupwNTVL7IbwkpUnQ=="
        go_signature = b"d1B8kLk7i+aUMWJsvkrOvuHwTdvB0HtQPhQiB44QoXgGHaTPOL4+kagobPhWvF61hGezzLn6qukv2UYV5R1/CQ=="
        go_message = b"charinko_locked_sate"


        self.assertTrue(ed25519.verify(
            go_message,
            go_signature,
            go_pubkey))

        self.assertTrue(crypto.verify(
            go_pubkey,
            go_signature,
            go_message
        ))

    def test_crypt_js(self):
        print("test_crypt_js")
        js_pubkey = b"IuoWmTU/dG7Q7O2mSEIQKnXbMTEJcko45gFqcu0tEWs="
        js_signature = b"+F6d6gKexVhzk0LUK6hkKuu76nc0Nt9RakrT4hu2Hkve8qzsz8jNvCuCuKvQN37OUNKqUh9lTMfBYPDFu2KGDQ=="
        js_message = b"dfc27cdbd6ec86613185e00afb27b11af2b8e2e8fc1573f80722a6e537cb06ab"
        self.assertTrue(ed25519.verify(
            js_message,
            js_signature,
            js_pubkey
        ))
        self.assertTrue(crypto.verify(
            js_pubkey,
            js_signature,
            js_message
        ))
