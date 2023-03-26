import jwt
import bcrypt
from flask import Flask, request, render_template, make_response, redirect, url_for, session
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
try:
    conn = psycopg2.connect(dbname="test")
    cur = conn.cursor()
    print("Connected to Postgres")
except Exception as e:
    print("An error occurred while connecting: ", e)

@app.route("/")
def index():
    return render_template("home.html") # use to test each html

@app.route('/login', methods =['POST','GET'])
def login():
    msg = ""
    if request.method == 'POST':
        # if request.form['password'] == 'admin':
        username = request.form['user_email'] 
        password = hp(request.form['password'])
        account = cur.execute("""SELECT * FROM user_login WHERE user_name=? AND hashed_password=?""", [username,password])
        if account:
            # session['loggedin'] = True
            # session['id'] = account['id']
            # session['username'] = account['username']
            msg = "Logged in successfully!"
            # render the home page maybe?
            return render_template("home.html",msg=msg)
        else:
            msg = "Incorrect username / password!"
    return render_template('login.html', msg = msg)

# may or may not implement this lol. not super important
@app.route('/logout', methods=['POST','GET'])
def logout():
    return
    

@app.route('/signup', methods=['POST','GET'])
def signup():
    msg = ""
    if request.method == 'POST':
        f_name = request.form['user_fname']
        l_name = request.form['user_lname']
        email = request.form['user_email']
        password = request.form['user_password']
        phone_number = request.form['phone_number']
        sex = request.form['sex']
        dob = request.form['dob']
        # address area
        line_1 = request.form['line_1']
        city = request.form['city']
        state = request.form['state']
        temp.insert_user(cur,f_name,l_name,(line_1,city,state), phone_number,sex, dob, 'NONE')

@app.get('/report_gifts')
def report_gifts():
    gift_name = request.args.get('gift-name')
    if gift_name:
        cur.execute("""
            SELECT i.gift_sku, i.gift_name, i.gift_price, DATE(s.gift_transaction_at)
            FROM gift_shop_item as i
            INNER JOIN gift_shop_sales as s 
            ON s.gift_sku = i.gift_sku 
            WHERE i.gift_name = %s""", [gift_name]
            )
        data = cur.fetchall()
        app.logger.info(data)
        return render_template('report_gifts.html', data=data)
    else:
         return render_template('report_gifts.html')
            
