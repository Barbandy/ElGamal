#! /usr/bin/python
# coding: UTF-8

import argparse
import random


def writeFile(fname, code):
    try:
        with open(fname, 'wb') as f:
            f.write(''.join(code))
    except IOError:
        exit('No such file or directory ' + fname)		

		
def readFile(fname):
    try:
        with open(fname, 'rb') as f:
            text = f.read()
    except IOError:
        exit('No such file or directory ' + fname)
    return text


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('inFile')
    parser.add_argument('outFile')
    parser.add_argument('mode', choices=['e', 'd'])
    return parser.parse_args()

	
# нахождение и проверка простого числа	
def PrimeN(bits):
    p = random.randint(2 ** (bits - 1), 2 ** bits)
    while not MillerRabin(p):
        p += 1
    return p	


# тест Миллера-Рабина
def MillerRabin(m):
    t = m - 1
    s = 0
    while t % 2 == 0:
        t /= 2
        s += 1
            
    for i in range(20):
        a = random.randint(2, m-2)
        x = pow(a, t, m)
        if x == 1:
            return True # составное
        for i in range(s - 1):
            x = (x ** 2) % m
            if x == m - 1:
                return True # составное
        return x == m - 1   # простое
				
		
# генерация ключей		
def KeyGen(bitlen):
    p = PrimeN(bitlen)
    g = random.randint(0, p)
    x =  random.randint(1, p-1)
    y = pow(g, x, p)
       
    pub_key = "{}\n{}\n{}".format(p, g, y)
    priv_key = "{}\n{}".format(x, p)

    return 	pub_key, priv_key, p, g, y


def encryption (g, m, p, y):
    k = random.randint(1, p - 1)
    a = pow(g,k,p)
    b = pow(y,k,p)
    b = (b *m)%p

    return a, b	
	
def decryption (a, b, p, x):
    return ((b * pow(a, p-1-x, p))% p)	
	
	
def main():
    print "Elgamal"
    bitlen = 2048
    kpub = "key.public"
    kpriv = "key.private"
    args = getArgs()
	
    if args.mode == 'e':
        pub_key, priv_key, p, g, y = KeyGen(bitlen)
        bytes = readFile(args.inFile)
        m =0
        for i, c in enumerate(bytes):
            m |= (ord(c) << i*8)

        a, b = encryption(g, m, p, y)
        writeFile(kpub, pub_key)
        writeFile(kpriv, priv_key)
        ab = "{}\n{}".format(a, b)
        writeFile(args.outFile, str(ab))
		
    if args.mode == 'd':
        f = open(kpriv)
        x = int(f.readline())
        p = int(f.readline())
        f.close()
		
        f = open(args.outFile)
        a = int(f.readline()) 
        b = int(f.readline()) 
        f.close()
        m = decryption(a, b, p, x)

        res = ""
        while m > 0:
            byte = m % 256
            res += chr(byte)
            m /= 256

        writeFile(args.outFile, res)

		
if __name__ == "__main__":
    main()	