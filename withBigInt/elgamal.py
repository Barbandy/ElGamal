#! /usr/bin/python
# coding: UTF-8

import argparse
import random
import BigInt


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('inFile')
    return parser.parse_args()

	
# проверка простого числа	
def Test_Prime(n):
    if not MillerRabin(n):
        raise ValueError("The selected number is not simple.")	

		
def powmod(a, k, n):
    res, aa, kk = BigInt.BigInt(1), a, k
    while kk != 0:
        if (kk % 2) == 1:
            res = (res * aa) % n
        aa = (aa * aa) % n
        kk /= 2
    return res
	

# тест Миллера-Рабина
def MillerRabin(m):
    m = m.getString()
    m = int(m)
    t = m - 1
    s = 0
    while t % 2 == 0:
        t /= 2
        s += 1
            
    for i in range(20):
        a = random.randint(1, m-1)
        x = pow(a, t, m)
        if x == 1:
            return True # составное
        for i in range(s - 1):
            x = pow(x, 2, m)
            if x == m - 1:
                return True # составное
        return x == m - 1   # простое
				
		
# генерация ключей		
def KeyGen(bitlen):
    p = BigInt.BigInt()
    p.getFrom_txt("p.txt")
    Test_Prime(p)

    g = random.randint(0, p)
    x =  random.randint(1, p-1)

    p = BigInt.BigInt(str(p))
    g = BigInt.BigInt(str(g))
    x = BigInt.BigInt(str(x))  
    y = powmod(g, x, p)
    pub_key = "{}\n{}\n{}".format(p, g, y)
    priv_key = "{}\n{}".format(x, p)

    return 	p, g, y, x


def encryption (g, m, p, y):
    k = random.randint(1, p - 1)
    a = powmod(g,k,p)
    b = powmod(y,k,p)
    b = (b * m)%p

    return a, b	
	
def decryption (a, b, p, x):
    return ((b * powmod(a, p-1-x, p))% p)	
	
	
def main():
    print "Elgamal"
    args = getArgs()
	msg = BigInt.BigInt()
    msg.getFrom_txt(args.inFile)

    p, g, y, x = KeyGen()
    print "text = ", msg
    msg = BigInt.BigInt(str(msg))
    a, b = encryption(g, msg, p, y)
    print "encrypt_text = ", c
    text = decryption(a, b, p, x)	
    print "decrypt_text = ", text
    
    if msg == text:
        print"Success!"
    else:
        print "Failure!"
    

		
if __name__ == "__main__":
    main()	