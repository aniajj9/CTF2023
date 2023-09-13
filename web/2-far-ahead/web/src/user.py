import json
import requests
import os
import tempfile
from werkzeug.security import check_password_hash

class User:
    def __init__(self, username : str, password : str, is_admin : bool = False, image : str = None):
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.image = image
        self.image_base_dir = os.getenv("PATH_PROFILE_IMAGES", "/tmp/")
    
    def is_valid_password(self, user_provided_password):
        return len(self.password) > 0 and check_password_hash(self.password, user_provided_password)

    def store_image(self, content):
        self.delete_image()

        with tempfile.NamedTemporaryFile(prefix = "img_", delete=False, dir=self.image_base_dir) as fp:
            fp.write(content)
            return fp.name

    def delete_image(self):
        if self.image is None:
            return None
        
        filename = os.path.join(self.image_base_dir, os.path.basename(self.image))
        if os.path.isfile(filename):
            os.unlink(filename)

    def get_image_contents(self):
        if not self.image:
            return None
        
        filename = os.path.join(self.image_base_dir, os.path.basename(self.image))
        try:
            with open(filename, "rb") as fp:
                return fp.read()
        except:
            return None
    
    def to_json(self):
        return json.dumps({"username": self.username, "password": self.password, "is_admin": self.is_admin, "image": self.image})
    
    @staticmethod
    def from_json(raw):
        data = json.loads(raw)
        data["image"] = os.path.basename(data["image"]) if data["image"] else None
        return User(data["username"], data["password"], data["is_admin"], data["image"])