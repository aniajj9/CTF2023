
import random

with open("/ctf/flag.txt", "r") as f:
    flag = f.read()

# Password reset functionality for my super secure new website
account_reset_token = None
admin_reset_token = None

# generate 128 bit random reset token
def GenerateToken():
    token =  hex(random.getrandbits(128))
    paddedtoken = token[2:].zfill(32)
    return paddedtoken

while True:
    print("Enter `1` to request a reset of your password.\nEnter 2 to request a reset of the admin password.\nEnter 3 to reset the admin password")
    choice = input("Choice: ")
    if choice == "1":
        reset_token = GenerateToken()
        account_reset_token = reset_token

        # you receive this email
        print(f"Your password reset token is: {account_reset_token}")
    if choice == "2":
        reset_token = GenerateToken()
        admin_reset_token = reset_token
        print(f"a password reset email has been sent to the admin account :)")
    if choice == "3":
        entered_token = input("Enter your password reset token: ")
        if entered_token == admin_reset_token:
            print(f"admin password reset! Well done, here's a flag: {flag}")
            exit()
        else:
            print("the token is invalid")
            exit()
