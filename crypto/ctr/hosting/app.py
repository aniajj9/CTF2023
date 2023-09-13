#!/usr/bin/env python3
from flask import Flask,request,Response,make_response
import json,os, sys
from Crypto.Cipher import AES
### Global variables
app = Flask(__name__)

secret_key = os.urandom(16)
ctr_nonce = os.urandom(8)

# Generate a secure cookie using MILITARY GRADE AES-128 ENCRYPTION
# Using CTR mode: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Counter_(CTR)
def gen_user_cookie():
    cookie_dict = {}
    cookie_dict["access_level"] = "User"
    pt = json.dumps(cookie_dict).encode()
    cipher = AES.new(secret_key, AES.MODE_CTR, nonce = ctr_nonce)
    ct = cipher.encrypt(pt).hex()
    return ct

def decrypt_admin_cookie(cookie):
    ct = bytes.fromhex(cookie)
    cipher = AES.new(secret_key, AES.MODE_CTR, nonce = ctr_nonce)
    pt = cipher.decrypt(ct)
    return pt
    
@app.route('/flag')
def retPsyduck():
    user_cookie = request.cookies.get('permissions')
    if user_cookie == None:
        return Response("No cookie set")
    try:
        decrypted = decrypt_admin_cookie(user_cookie)
    except:
        return Response("Something went wrong decrypting your cookie")
    try:
        cookie_dict = json.loads(decrypted.decode())
        allowed = cookie_dict["access_level"] == "Admin"
    except:
        return Response(f"Failed to parse decrypted cookie: {decrypted.hex()}")


    if allowed: 
        with open('images/flag.png','rb') as f:
                return Response(f.read(), mimetype='image/png')
    else:
        return Response(f"This page is for admins only! Your cookie was: {decrypted.hex()}")


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
