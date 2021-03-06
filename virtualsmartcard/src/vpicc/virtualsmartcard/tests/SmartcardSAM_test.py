import unittest
from virtualsmartcard.SmartcardSAM import *

#Unit Tests   
class TestSmartcardSAM(unittest.TestCase):

    def setUp(self):
        self.password = "DUMMYKEYDUMMYKEY"
        self.myCard = SAM("1234", "1234567890")

    def test_incorrect_pin(self):
        with self.assertRaises(SwError):
            self.myCard.verify(0x00, 0x00, "5678")

    def test_counter_decrement(self):
        ctr1 = self.myCard.counter
        try:
            self.myCard.verify(0x00, 0x00, "3456")
        except SwError as e:
            pass
        self.assertEquals(self.myCard.counter, ctr1 - 1)

    def test_internal_authenticate(self):
        sw, challenge = self.myCard.get_challenge(0x00, 0x00, "")
        print("Before encryption: " + challenge)
        blocklen = vsCrypto.get_cipher_blocklen("DES3-ECB")
        padded = vsCrypto.append_padding(blocklen, challenge)
        sw, result_data = self.myCard.internal_authenticate(0x00, 0x00, padded)
        print("Internal Authenticate status code: %x" % sw)
        self.assertEquals(sw, SW["NORMAL"])

    def test_external_authenticate(self):
        sw, challenge = self.myCard.get_challenge(0x00, 0x00, "")
        print("Before encryption: " + challenge)
        blocklen = vsCrypto.get_cipher_blocklen("DES3-ECB")
        padded = vsCrypto.append_padding(blocklen, challenge)
        sw, result_data = self.myCard.internal_authenticate(0x00, 0x00, padded)
        sw, result_data = self.myCard.external_authenticate(0x00, 0x00, result_data)
        print ("After external authenticate: " + result_data)
        self.assertEquals(sw, SW["NORMAL"])

if __name__ == "__main__":
    unittest.main()
    #SE = Security_Environment(None)
    #testvektor = "foobar"
    #print "Testvektor = %s" % testvektor
    #sw, hash = SE.hash(0x90,0x80,testvektor)
    #print "SW after hashing = %s" % sw
    #print "Hash = %s" % hash
    #sw, crypted = SE.encipher(0x00, 0x00, testvektor)
    #print "SW after encryption = %s" % sw
    #sw, plain = SE.decipher(0x00, 0x00, crypted)
    #print "SW after encryption = %s" % sw
    #print "Testvektor after en- and deciphering: %s" % plain
    #sw, pk = SE.generate_public_key_pair(0x02, 0x00, "")
    #print "SW after keygen = %s" % sw
    #print "Public Key = %s" % pk
    #CF = CryptoflexSE(None)
    #print CF.generate_public_key_pair(0x00, 0x80, "\x01\x00\x01\x00")
    #print MyCard._get_referenced_key(0x01)
