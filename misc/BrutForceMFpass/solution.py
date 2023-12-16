"""
The task:
    Given a hash of a simple password (lowercase + numbers, max 6 or 8 characters - MF password):
        See that its easy to bruteforce
Create the task for the participants:
    1. Find an easy password (lowercase + numbers, max 6 or 8 characters - MF password)
    2. Hash it using any hash function, for example sha-256 (that's what I used in the example)
    3. Give the users the hash to bruteforce
    4. Suggest bruteforce by telling that password is short and contains only lowercase and numbers
    5. Prepare a way for them to obtain the flag. For example a simple input form, where the MF password will be inputted
Possible solution:
    Write a simple script that:
        1. Creates all possible password combinations that meet the requirements
        2. Hashes the created password (participants can see what type of hash is used, using for example online solutions)
        3. Compares if the two strings are the same
DO NOT UPLOAD FOR THE PARTICIPANTS

Below is an example solution, working as a poc that:
    - Bruteforcing is feasible within a reasonable time
    - The task works as expected
"""

import string
import itertools
from hashlib import sha256
import time


if __name__ == '__main__':
    start = time.time()

    hashPassword = "75e5dcbe410b4739e9ba40e0e7effea1e7a7bcd8567f22fe876eb6ae8ca0d7f3"  # Solution: sz3r1
    # TODO: How to hint to the users that it consists only a few lowercase and numbers? Literally hint that its
    #  mainframe password??

    # A simple brute forcer: given up to x characters, and lower case and numbers only, make a password, hash it,
    # and compare it with a hash The type of hash can be found using fex some online hash type finders

    for length in range(1, 7): # TODO: Check how long it takes to bruteforce. A few minutes sounds ok, a few hours - not so much
        for possible_password in itertools.product((string.digits + string.ascii_lowercase), repeat=length):
            password = ''.join(map(str, possible_password))
            if sha256(password.encode('utf-8')).hexdigest() == hashPassword:
                print(password)
                break

    end = time.time()
    print(end - start)
