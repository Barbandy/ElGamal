#coding: UTF-8
import random, pytest, elgamal, BigInt

def test_elgamal():
    bitlen = 1024
    pub_key, priv_key, p, g, y, x = elgamal.KeyGen(bitlen)
    msg = BigInt.GenerateRandomMax(p-4)
    msg = BigInt.BigInt(str(msg))
    a, b = elgamal.encryption(g, msg, p, y)
    text = elgamal.decryption(a, b, p, x)
    assert msg == text

	


