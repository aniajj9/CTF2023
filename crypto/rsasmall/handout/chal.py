# pip install pycryptodome
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
import os

p,q = getPrime(1024), getPrime(1024)
n = p*q

e = 3

with open("flag.txt", "rb") as f:
    flag = f.read()

assert len(flag) == 31
# pad flag
int_flag = bytes_to_long(flag)

ct = pow(int_flag, e, n)

print(f'n = {n}')
print(f'e = {e}')
print(f'ct = {ct}')