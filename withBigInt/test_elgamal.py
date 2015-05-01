#coding: UTF-8
import random, pytest, elgamal, BigInt


def GeneratePrime(bitLen):
    p = BigInt.GenerateRandomLen(bitLen)
    while not rsa.MillerRabin(p):
        p += 1
    return p


def test_elgamal():
    msg = BigInt.BigInt()
    p = BigInt.BigInt()
    p = GeneratePrime(1024)
   #///...///
    assert msg == text

	



