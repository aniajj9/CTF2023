from Crypto.Util.number import long_to_bytes

with open("output.txt", "r") as f:
    f.readline()
    N = int(f.readline()[3:].strip())
    e = int(f.readline()[3:].strip())
    f.readline()
    f.readline()
    f.readline()
    d = int(f.readline()[3:].strip())
    f.readline()
    ct = int(f.readline()[4:].strip())

print(long_to_bytes(pow(ct,d,N)))