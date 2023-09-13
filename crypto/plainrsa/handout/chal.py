# pip install pycryptodome
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes


# https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Key_generation
def rsaKeyGen(bitlen):
    P = getPrime(bitlen)
    Q = getPrime(bitlen)
    N = P * Q
    e = 65537
    phi = (P-1) * (Q - 1)
    d = pow(e,-1,phi)
    return (N,e), (P,Q,d)

# https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Encryption
def rsaEncrypt(msg, N, e):
    m = bytes_to_long(msg.encode())
    ct = pow(m,e,N)
    return ct

# https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Decryption
def rsaDecrypt(ct,N,e,P,Q,d):
    # i forgot how this works, can you help reimplement it?
    # i forgot how this works, can you help reimplement it?
    # i forgot how this works, can you help reimplement it?
    return long_to_bytes(m)


with open("flag.txt", "r") as f:
    flag = f.read()

pubkey, privkey = rsaKeyGen(512)
N,e = pubkey
P,Q,d = privkey

ct = rsaEncrypt(flag, N, e)

print(f'public key:')
print(f'N = {N}')
print(f'e = {e}')
print(f'private key:')
print(f'P = {P}')
print(f'Q = {Q}')
print(f'd = {d}')

print("encrypted flag")
print(f'ct = {ct}')
