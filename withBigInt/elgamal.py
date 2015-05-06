﻿#! /usr/bin/python
# coding: UTF-8

import argparse
import random
import BigInt


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('inFile')
    parser.add_argument('outFile')
    parser.add_argument('mode', choices=['e', 'd'])
    return parser.parse_args()

def GeneratePrime(bitLen):
    p = BigInt.GenerateRandomLen(bitLen)
    while not MillerRabin(p):
        p += 1
    return p

	
# тест Миллера-Рабина
def MillerRabin(m):
    m = m.getString()
    m = int(m)
    t = m - 1
    s = BigInt.BigInt(0)
    while t % 2 == 0:
        t /= 2
        s += 1
            
    for i in range(20):
        #a = BigInt.GenerateRandomMax(m-4)+2
        a = random.randint(1, m-1)
        x = pow(a,t,m)#m.powmod(a, t, m)
        if x == 1:
            return True # составное
    i = BigInt.BigInt(0)
    while i < s - 1:
        x = (x * x) % m
        if x == m - 1:
            return True
        i = i + 1
    return x == m - 1
				
		
# генерация ключей		
def KeyGen(bitlen):
    p = GeneratePrime(bitlen)
    g = BigInt.GenerateRandomMax(p)
    x = BigInt.GenerateRandomMax(p)
    y = p.powmod(g,x,p)
    pub_key = "{}\n{}\n{}".format(p, g, y)
    priv_key = "{}\n{}".format(x, p)
    return pub_key, priv_key, p, g, y, x


def encryption (g, m, p, y):
    m = BigInt.BigInt(str(m))
    if m >= p:
        raise ValueError('Message is too large!')
    
    k = BigInt.GenerateRandomMax(p-2)+1
    a = p.powmod(g,k,p)
    b = p.powmod(y,k,p)
    b = (b * m ) % p

    return a, b	
	
	
def decryption (a, b, p, x):
    return ((b * p.powmod(a, p-1-x, p) %p))	
	
	
def main():
    print "Elgamal"
    args = getArgs()
    bitlen = 1024
    BigInt.initRandom()
    with open(args.inFile) as f:
            msg = int(f.read()) 
    if args.mode == 'e':
        pub_key, priv_key, p, g, y, x = KeyGen(bitlen)
        msg = BigInt.BigInt(str(msg))
        a, b = encryption(g, msg, p, y)
        ab = "{}\n{}".format(a, b)
        with open(args.outFile, 'w') as f:
            f.write(ab)
        with open('pub.key', 'w') as pub:
            pub.write(pub_key)
        with open('priv.key', 'w') as priv:
            priv.write(priv_key)

    if args.mode == "d":   
        with open(args.outFile) as f:
            (a, b) = f.read().split("\n") 
        a = BigInt.BigInt(a)
        b = BigInt.BigInt(b) 
        with open('priv.key') as priv:
            (x, p) = priv.read().split("\n") 
        x = BigInt.BigInt(x)
        p = BigInt.BigInt(p)   
        text = decryption(a, b, p, x)
        text.saveTo_txt("res.txt")
    			
if __name__ == "__main__":
    main()	