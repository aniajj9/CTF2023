from user import User
import os
from werkzeug.security import generate_password_hash
import pyotp

class UserDatabase:
    def __init__(self, redis):
        self.redis = redis
        self.register(User(os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD"), True))
    
    def register(self, user: User):
        user.password = generate_password_hash(user.password)
        result = self.redis.set("user_" + user.username, user.to_json(), nx=True)
        return result == True
    
    def get_by_name(self, username: str):
        result = self.redis.get("user_" + username)

        if not result:
            return None
        
        return User.from_json(result)
    
    def update(self, user: User):
        result = self.redis.set("user_" + user.username, user.to_json())
        return result == True

class TOTPDatabase:
    def __init__(self, redis):
        self.redis = redis
    
    def __get_token_secret(self, user: User):
        return self.redis.get("totp_" + user.username)

    def is_valid(self, user: User, code: str):
        secret = self.__get_token_secret(user)
        if not secret or type(code) != str or code is None or len(code) != 8:
            return False
        
        totp = pyotp.TOTP(secret, digits=8, interval=30)
        return totp.verify(code)

    def is_enrolled(self, user: User):
        secret = self.__get_token_secret(user)
        return secret != None
    
    def enroll(self, user: User):
        secret = pyotp.random_base32()
        return self.redis.set("totp_" + user.username, secret, nx=True) == True