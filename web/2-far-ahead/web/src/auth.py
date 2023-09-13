from functools import wraps
from user import User
from flask import g, request, redirect, url_for, session
import os
import pickle
import base64
import hmac
import hashlib
from typing import Optional
from database import UserDatabase

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for('login'))
        
        if "missing_2fa" in session:
            return redirect(url_for('form_2fa'))

        return f(*args, **kwargs)
    return decorated_function

def no_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function