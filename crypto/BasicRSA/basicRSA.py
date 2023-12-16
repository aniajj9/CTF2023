# Basic RSA scheme, with key generation
# Challenge: decrypt ciphertext given private, public key
# Flag is plaintext
from Crypto.Util.number import getPrime, inverse  # pip install pycryptodome


# Generate public and private RSA key
# key_bits - bit size of n
def generate_keys(n_bits: int):
    assert n_bits > 0
    k_bits = n_bits // 2
    p = getPrime(k_bits)
    q = getPrime(k_bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = inverse(e, phi)
    public_key = (n, e)
    private_key = (n, d)
    return public_key, private_key


# RSA encryption of an integer under public key
def RSA_encrypt(message: int, public_key) -> int:
    n, e = public_key
    assert 0 <= message < n
    return pow(message, e, n)


# RSA decryption of integer under private key
def RSA_decrypt(ciphertext: int, private_key) -> int:
    n, d = private_key
    assert 0 <= ciphertext < n
    return pow(ciphertext, d, n)


def string_to_int(message: str) -> int:
    return int(message.encode('utf-8').hex(), 16)


def int_to_string(message: int) -> str:
    message_hex = hex(message)[2:]
    return bytes.fromhex(message_hex).decode('utf-8')


# What will be presented for the challenge
def challenge_info():
    pub_k, priv_k = generate_keys(1024)
    message = "flag......"
    cipher = RSA_encrypt(string_to_int(message), pub_k)
    return pub_k, priv_k, cipher


if __name__ == '__main__':
    pub_k, priv_k, cipher = challenge_info()
    plain = int_to_string(RSA_decrypt(cipher, priv_k))
    print(plain)
