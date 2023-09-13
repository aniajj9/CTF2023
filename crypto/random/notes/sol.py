import random, time
# pip install randcrack
from randcrack import RandCrack
from pwn import *

rc = RandCrack()

# with process(["python3 chal.py"], shell=True, level="debug") as r:
with remote("127.0.0.1",1337, level="debug") as r:
    for i in range(624//4):
        r.sendline("1")
        r.recvuntil(b'Your password reset token is: ')
        token = r.readline().strip().decode()
        outputs = [int(token[8*i:8*i + 8],16) for i in range(4)][::-1]
        # print(outputs)
        for x in outputs:
            rc.submit(x)

    r.sendline("2")
    r.recvuntil(b'a password reset email has been sent to the admin account :)')
    r.sendline("3")
    r.recvuntil(b'Enter your password reset token: ')
    token = ""
    for i in range(4):
        token = hex(rc.predict_randrange(0,4294967295))[2:].zfill(8) + token

    r.sendline(token)
    r.interactive()