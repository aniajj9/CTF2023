import subprocess
import base64
import os

def pack(name, content, delete=False):
    subprocess.check_output(["zip", "-Ar", name, content])
    if delete:
        os.unlink(content)

def unlink(zipfile, filename):
    subprocess.check_output(["zip", "-Ad", zipfile, filename])

n = 2
flag = "CTF{That_was_a_lot_of_files_huh_such_is_the_way_of_the_matryoshka_chal!!}"
encoded = base64.b64encode(flag.encode()).decode()
chunks = [encoded[i:i+n] for i in range(0, len(encoded), n)]
chunks = chunks[::-1]

print("[+] Encoded: ", encoded)
pack(chunks[0], 'think.jpg', delete=False)
unlink(chunks[0], 'think.jpg')

for idx in range(1, len(chunks)):
    target = chunks[idx - 1]
    source = chunks[idx]
    print(target, " goes into ", source)
    pack(source, target, delete=True)

pack("starthere.zip", chunks[-1], delete=True)