import requests
from pwn import xor
import json
targeturl = "http://127.0.0.1"
targetport = 5000

sess = requests.session()

# get cookie
res = sess.get(targeturl + ":" +str(targetport))

# extract cookie
cookie = sess.cookies.get_dict()["permissions"]

print(f"originalcookie {cookie}")
IV, cookie = cookie.split("--")

# create modified cookie
cookie = bytes.fromhex(cookie)[:16]
IV = bytes.fromhex(IV)
currentcookie = b'{"admin": false}'
requiredcookie = b'{"admin": true}\x01'
newIV = xor(currentcookie, xor(requiredcookie,IV))

newcookie = newIV.hex() + "--" + cookie.hex()
# set new cookie
sess.cookies.set("permissions", newcookie)

# get png of flag from endpoint


# res = sess.get(targeturl + ":" + str(targetport) + "/flag")
# res = requests.get(targeturl + ":" + str(targetport) + "/flag")
print(f'new cookie {newcookie}')
res = requests.get(targeturl + ":" + str(targetport) + "/flag", cookies={'permissions': newcookie})
# print(bytes.fromhex(res.text.split(" ")[-1]))
# decode and save image to file
# print(res.text)
res.raw.decode_content = True
with open("flag.png", "wb") as f:
    for x in res:
        f.write(x)