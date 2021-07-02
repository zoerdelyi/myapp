import bcrypt
import os
from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + \
                          os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']

mongo = PyMongo(app)
db = mongo.db
records = db.register


@app.route("/", methods=['post', 'get'])
def index():
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                flash('Wrong password!')
                return render_template('index.html')
        else:
            flash('Email not found!')
            return render_template('index.html')
    return render_template('index.html')


@app.route("/signup", methods=['post', 'get'])
def signup():
    if "email" in session:
        flash('Sign out first!')
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            flash('There is already a user by that name!')
            return render_template('signup.html')
        if email_found:
            flash('This email is already exists in database!')
            return render_template('signup.html')
        if password1 != password2:
            flash('Passwords should match!')
            return render_template('signup.html')
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            records.insert_one(user_input)
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            return render_template('signed_up.html', email=new_email)
    return render_template('signup.html')


@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('logged_in.html', email=email)
    else:
        flash('You are not signed in!')
        return redirect(url_for("index"))


@app.route('/signed_up')
def signed_up():
    return render_template('signed_up.html')


@app.route("/logout", methods=['post', 'get'])
def logout():
    if "email" in session:
        session.pop("email", None)
        flash('You have signed out!')
    else:
        flash('You are not signed in!')
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.secret_key = 'tgmRnLMKikIoQW0qz3mx'
    app.run(host='0.0.0.0', port=5000, debug=False)
