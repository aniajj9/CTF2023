"""
Code to provide an input field to check for the mainframe password and provide a flag
It implements increasing timeout, to lead the participants away from trying to bruteforce password here, without using hash


subfile wth password protected, containig flag - LOCAL
"""
import time

TIMEOUT = 2  # Initial timeout [s]
TIMEOUT_INCREASE = TIMEOUT # Factor by which timeout will increase with each wrong password
INVALID_PASSWORD_MSG = "Wrong password"


def login():
    global TIMEOUT

    while True:
        print("Input password to login:")
        password = input()
        if password == "ge94s":
            print("Congratulations! Here's the flag: \nCTF{...}")
            break
        print(f"Timeout: {TIMEOUT} seconds\n")
        time.sleep(TIMEOUT)
        TIMEOUT *= TIMEOUT_INCREASE


if __name__ == '__main__':
    login()
