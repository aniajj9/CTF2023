# --- The task: ---
# Participants are given a hash (same for all), and the source code. The task is to:
# 1. Reverse the hash (hash should be in online md5 reverse calculators)
# 2. Analyse the encryption code
# 3. Notice that the only step in which the password is encoded is by mapping characters
# 4. Map the characters and get the flag
# 5. I think this task is quite easy, difficulty could be added by making lines prior to mapping actually change sth
# 6. This could also be made in a more "complicated" language

import hashlib
import string
import random


def encrypt(plaintext):
    randomness = ''.join(random.choices(string.ascii_lowercase +
                                        string.digits, k=len(plaintext)))
    ciphertext = ""
    for i in range(len(plaintext)):
        ciphertext += chr(ord(plaintext[i]) % 256)  # This does nothing to the ciphertext
    # XOR plaintext with randomness
    ciphertext = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(ciphertext, randomness))
    ciphertext = list(ciphertext)
    ciphertext = "".join(ciphertext)
    # XOR again with the same randomness (same, since a xor b xor b = a)
    ciphertext = bytes([_a ^ _b for _a, _b in zip(ciphertext.encode(), randomness.encode())]).decode()
    mapping = {
        "a": "e",
        "b": "O",
        "c": "y",
        "d": "8",
        "e": "3",
        "f": "u",
        "g": "6",
        "h": "k",
        "i": "9",
        "j": "1",
        "k": "h",
        "l": "7",
        "m": "0",
        "n": "5",
        "o": "t",
        "p": "r",
        "q": "2",
        "r": "s",
        "s": "l",
        "t": "o",
        "u": "4",
        "v": "1",
        "w": "2",
        "x": "0",
        "y": "a",
        "z": "4",
        "A": "T",
        "B": "V",
        "C": "Y",
        "D": "H",
        "E": "t",
        "F": "U",
        "G": "J",
        "H": "K",
        "I": "N",
        "J": "L",
        "K": "X",
        "L": "Z",
        "M": "P",
        "N": "Q",
        "O": "D",
        "P": "R",
        "Q": "F",
        "R": "R",
        "S": "a",
        "T": "O",
        "U": "G",
        "V": "S",
        "W": "B",
        "X": "E",
        "Y": "W",
        "Z": "I",
        "0": "F",
        "1": "C",
        "2": "M",
        "3": "E",
        "4": "N",
        "5": "A",
        "6": "D",
        "7": "B",
        "8": "X",
        "9": "Z",
        ",": "h",
        ".": "i",
        "-": "j",
        "_": "m",
        "{": "A",
        "}": "E",
        "(": "P",
        ")": "Q"
    }
    return "".join(mapping[x] for x in ciphertext)


def string_to_int(message: str) -> int:
    return int(message.encode('utf-8').hex(), 16)


def int_to_string(message: int) -> str:
    message_hex = hex(message)[2:]
    return bytes.fromhex(message_hex).decode('utf-8')


if __name__ == '__main__':
    plain = "ctf{paSs_brEAkeR}"
    print(encrypt(plain)) # 1st password
    print(hashlib.md5(encrypt(plain).encode()).hexdigest()) # the hash'''

#    The MD5 hash:
#       433ef195050140611519331ddd103b5c
#    was successfully reversed into the string:
#       youArealmOstTh3RE
#    The flag:
#       ctf{paSs_brEAkeR}
