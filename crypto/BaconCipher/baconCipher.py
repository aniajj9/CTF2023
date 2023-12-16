# Bacon cipher encryption https://en.wikipedia.org/wiki/Bacon%27s_cipher (Version with all distinct letter mapping)
import json
import re


# Bacon cipher encryption - encrypts alphabetic characters, and leaves other unchanged
def bacon_encrypt(plain: str) -> str:
    with open("plain_to_bacon.json") as f:
        data = json.load(f)
    return "".join(data[x.upper()] if x.isalpha() else x for x in plain)


# Bacon cipher decryption - decrypts alphabetic characters as uppercase, leaves other unchanged
def bacon_decrypt(cipher: str) -> str:
    with open("bacon_to_plain.json") as f:
        dictionary = json.load(f)

    pattern = re.compile('|'.join(map(re.escape, dictionary.keys())))

    def replace(match):
        return dictionary[match.group(0)]

    return pattern.sub(replace, cipher)


if __name__ == '__main__':
    plain = "When it comes to secrets, the Bacon cipher sizzles with mystery, making messages as tantalizing as crispy bacon strips. CTF{CrispyCryptographyConqueror}"
    cipher = bacon_encrypt(plain)
    print(cipher)
    decryption = bacon_decrypt(cipher)
    print(decryption)
    assert plain.upper() == decryption


