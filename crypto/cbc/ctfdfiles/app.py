#!/usr/bin/env python3
from flask import Flask,request,Response,make_response
import json,os, sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
### Global variables
app = Flask(__name__)

secret_key = os.urandom(16)


# Super secure MILITARY GRADE AES-128 encryption using CBC mode!
# https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC)
def gen_user_cookie():
    cookie_dict = {}
    cookie_dict["admin"] = False
    pt = json.dumps(cookie_dict).encode()
    padded_pt = pad(pt,16)
    CBC_IV = os.urandom(16)
    cipher = AES.new(secret_key, AES.MODE_CBC, IV = CBC_IV)
    ct = CBC_IV.hex() + "--" + cipher.encrypt(padded_pt).hex()
    return ct


def decrypt_admin_cookie(cookie):
    hexIV, hexct = cookie.split("--")
    CBC_IV, ct = bytes.fromhex(hexIV), bytes.fromhex(hexct)
    cipher = AES.new(secret_key, AES.MODE_CBC, IV = CBC_IV)
    padded_pt = cipher.decrypt(ct)
    return padded_pt
    
@app.route('/flag')
def retPsyduck():
    user_cookie = request.cookies.get('permissions')
    if user_cookie == None:
        return Response("No cookie set")
    try:
        padded_pt = decrypt_admin_cookie(user_cookie)
    except:
        return Response("Something went wrong decrypting your cookie")
    try:
        pt = unpad(padded_pt, 16)
        cookie_dict = json.loads(pt.decode())
        allowed = cookie_dict["admin"] == True
    except:
        return Response(f"Failed to parse decrypted cookie: {padded_pt.hex()}")


    if allowed: 
        with open('images/flag.png','rb') as f:
                return Response(f.read(), mimetype='image/png')
    else:
        return Response(f"This page is for admins only! Your cookie was: {pt.hex()}")


@app.route("/")
def index():
    res = make_response()
    cookie = gen_user_cookie()
    res.set_cookie('permissions', cookie)
    with open('./templates/index.html') as f:
        res.set_data(f.read())
    return res



if(__name__ == '__main__'):
    app.run(host='0.0.0.0')
