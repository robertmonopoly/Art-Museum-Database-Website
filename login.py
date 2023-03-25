import jwt
import bcrypt
import flask
from flask import Flask, request, render_template, make_response, redirect, url_for
app = Flask(__name__)
import psycopg2
import template as temp
import hash_password as hp
# MAIN IDEA
# 1. the user can send their email and password to the server
# 2. the server can validate the email and password, and see if it matches
# 3. the server can inform the user of if their username/password was correct

# OVERALL PROCESS:
# 1. user sends email/pw to server
# 2. server validates using bcrypt, if its valid then generates a JWT and sends it back 
# 3. JWT is set as a cookie
# 4. all future requests can grab the JWT from the browser cookies, and verify it, and then grab the info from the payload

conn = psycopg2.connect(dbname="test")
cur = conn.cursor()
print("Connected to Postgres")

@app.route("/")
def index():
    return render_template("login.html")

@app.route('/login', methods =['POST','GET'])
def login():
    msg = ""
    if request.method == 'POST':
        # if request.form['password'] == 'admin':
        username = request.form['user_email'] 
        password = hp(request.form['password'])
        if (cur.execute("""SELECT * FROM user_login WHERE user_name=? AND hashed_password=?""", [username,password])):
            msg = "Logged in successfully!"
            # render the home page maybe?
            return render_template("home.html")
        else:
            msg = "Incorrect username / password!"
    return render_template('login.html', msg = msg)


# @app.route('/home', methods = ['POST', 'GET'])
# def home():
#     if 