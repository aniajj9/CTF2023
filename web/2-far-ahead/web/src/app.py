from flask import Flask, render_template, redirect, url_for, request, flash, session, g, make_response
from database import UserDatabase, TOTPDatabase
import auth
from user import User
import os
import requests
import redis

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET")

redis = redis.Redis(host='redis', port=6379, db=0)
users = UserDatabase(redis)
totp = TOTPDatabase(redis)

@app.before_request
def init_context():
    g.messages = []
    g.user = users.get_by_name(session["user"]) if "user" in session else None

@app.route('/profile/image')
@auth.login_required
def profile_image():
    fallback = redirect(url_for('static', filename='images/profile.jpg'))
    
    if not g.user:
        return fallback

    image = g.user.get_image_contents()
    
    if not image:
        return fallback
    
    response = make_response(image)
    return response

@app.route('/profile', methods=['GET','POST'])
@auth.login_required
def change_profile_image():
    if request.method == 'POST':
        url = request.form.get('url')
        
        if not url:
            g.messages.append(["Please provide a valid url!", "danger"])
            return render_template('profile_image.html')
        
        if "http://" not in url.lower() and "https://" not in url.lower():
            g.messages.append(["Only supports http and https url's!", "danger"])
            return render_template('profile_image.html')
        
        try:

            result = requests.get(url)
            if result == None:
                g.messages.append([f"Image not found!", "danger"])
                return render_template('profile_image.html')

            filename = g.user.store_image(result)
            g.user.image = filename
            users.update(g.user)

            g.messages.append([f"Profile image saved", "success"])
            return redirect(url_for("index"))

        except Exception as err:
            g.messages.append(["Failed to change profile image!", "danger"])
            return render_template('profile_image.html')

    return render_template('profile_image.html')

@app.route('/login', methods=['GET','POST'])
@auth.no_login_required
def login():
    if "user" in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if (not username) or (not password):
            g.messages.append(["Please fill out all fields!", "danger"])
            return render_template('login.html')

        user = users.get_by_name(username)
        if user and user.is_valid_password(password):
            session["user"] = user.username

            if user.is_admin:
                session["missing_2fa"] = True
            elif "missing_2fa" in session:
                del session["missing_2fa"]

            return redirect(url_for('index'))

        g.messages.append(["Invalid username and/or password", "danger"])
        return render_template('login.html')

    return render_template('login.html')

@app.route('/login/2fa', methods=['POST'])
def enter_2fa():
    if "user" not in session:
        return redirect(url_for('login'))

    code = request.form.get('code')
    if not code:
        g.messages.append(["Please enter an OTP", "danger"])
        return render_template('2fa.html')

    if not totp.is_valid(g.user, code):
        g.messages.append(["Invalid OTP. Try again", "danger"])
        return render_template('2fa.html')

    del session["missing_2fa"]
    g.messages.append(["Your 2FA login is accepted", "success"])
    return redirect(url_for("index"))


@app.route('/login/2fa')
def form_2fa():
    if "user" not in session:
        return redirect(url_for('login'))

    if not totp.is_enrolled(g.user):
        return render_template('2fa_missing.html')

    return render_template('2fa.html')

@app.route('/register', methods=['GET','POST'])
@auth.no_login_required
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if (not username) or (not password) or (not password2):
            g.messages.append(["Please fill out all fields!", "danger"])
            return render_template('register.html')

        if len(username) > 20:
            g.messages.append(["Username is too long!", "danger"])
            return render_template('register.html')

        if password != password2:
            g.messages.append(["The provided passwords must be identical!", "danger"])
            return render_template('register.html')

        if users.register(User(username, password)):
            g.messages.append(["Account created", "success"])
            return render_template('login.html')
        else:
            g.messages.append(["Username is already taken", "danger"])

        return render_template('register.html')

    return render_template('register.html')

@app.route("/logout")
def logout():
    if "user" in session:
        del session["user"]
    return redirect(url_for('index'))

@app.route("/")
@auth.login_required
def index(): 
    return render_template("index.html", flag=os.getenv("FLAG"))