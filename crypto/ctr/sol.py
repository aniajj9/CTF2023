import requests
from pwn import xor
import json
targeturl = "http://127.0.0.1"
targetport = 8000

sess = requests.session()

# get cookie
res = sess.get(targeturl + ":" +str(targetport))

# extract cookie
cookie = sess.cookies.get_dict()["permissions"]

# create modified cookie
cookie = bytes.fromhex(cookie)
currentcookie = b'{"access_level": "User"}'
requiredcookie = b'{"access_level":"Admin"}'
newcookie = xor(currentcookie, xor(requiredcookie,cookie))

# set new cookie
sess.cookies.set("permissions", newcookie.hex())

# get png of flag from endpoint
res = sess.get(targeturl + ":" + str(targetport) + "/flag")

# decode and save image to file
res.raw.decode_content = True
with open("flag.png", "wb") as f:
    for x in res:
        f.write(x)