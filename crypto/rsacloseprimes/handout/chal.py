# pip install pycryptodome
from Crypto.Util.number import isPrime, getPrime, bytes_to_long, long_to_bytes
import os

p = getPrime(1024)
x = p + 2**256


while True:
    if isPrime(x):
        q = x
        break
    else:
        x += 1

n = p*q

e = 65537

with open("flag.txt", "rb") as f:
    flag = f.read()

# pad flag
int_flag = bytes_to_long(flag)

ct = pow(int_flag, e, n)

print(f'n = {n}')
print(f'e = {e}')
print(f'ct = {ct}')