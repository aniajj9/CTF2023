# Basic RSA scheme, with key generation
# First prime p (n=pq) is small - it is possible to iterate through small primes to get the private exponent
from Crypto.Util.number import getPrime, inverse  # pip install pycryptodome


# Generate public and private RSA key
# p_bits - bit size of one factor of n
# n_bits - bit size of n
def generate_keys(p_bits: int, n_bits: int):
    assert n_bits > p_bits > 0
    q_bits = n_bits - p_bits
    p = getPrime(p_bits)
    q = getPrime(q_bits)
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


# ----------------------------------------------------------------------------
# Function to bruteforce p
# Message - int ciphertext to decrypt
# p_max_bits - max bit size of p
def decipher_without_private_key(message: int, public_key, p_max_bits=None):
    n, e = public_key
    assert 0 <= message < n

    def compute_private_exponent(p: int):
        q = n // p
        phi = (p - 1) * (q - 1)
        d = inverse(e, phi)
        return d

    if p_max_bits is None:
        p_max_bits = n.bit_length() - 1

    for p in range(2, (2 ** p_max_bits)):
        private_key_candidate = (n, compute_private_exponent(p))
        plaintext = RSA_decrypt(message, private_key_candidate)
        try:
            plaintext = int_to_string(plaintext)
            return plaintext
        except ValueError:
            continue


if __name__ == '__main__':
    pub_k, priv_k = generate_keys(10, 1024)
    print(pub_k)
    message = "Congratulations warrior, the flag is yours: CTF{sm4ll_pr1mes_mak3_h4ckers_hapPY}"

    # Test basic encryption - decryption
    cipher = RSA_encrypt(string_to_int(message), pub_k)
    print(cipher)
    plain = int_to_string(RSA_decrypt(cipher, priv_k))
    assert message == plain

    # Try to bruteforce the private key
    plain_bruteforce = decipher_without_private_key(cipher, pub_k)
    print(plain_bruteforce)
    assert message == plain

