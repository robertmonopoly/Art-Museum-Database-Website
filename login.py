from flask import Flask, request, render_template, make_response, redirect, url_for, session
import psycopg2
import template as temp
import hash_password as hp
app = Flask(__name__)
app.secret_key = 'my_secret'

# USER CLASS
class User():
    def __init__(self, name, email, password, access='USER'):
        self.name = name
        self.email = email
        self.password = password
        self.access = access
# Connection
try:
    conn = psycopg2.connect(dbname="test")
    cur = conn.cursor()
    print("Connected to Postgres")
except Exception as e:
    print("An error occurred while connecting: ", e)

@app.route("/")
def index():
    return render_template("login.html") 

@app.route('/home', methods = ['POST', 'GET'])
def home():
    if request.method == 'GET':
        user = request.cookies.get('user-role')
        return render_template("home.html", user=user)

@app.route('/login', methods =['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['user_email'] 
        in_password = request.form['password']
        try:
            cur.execute("""SELECT hashed_password FROM user_login WHERE user_name= %s""", (email,))
            db_password = cur.fetchone()
        except psycopg2.Error as e:
            print("error",e)
    
        valid_password = hp.isValidPw(in_password,db_password)
        print (valid_password)

        if valid_password:
            cur.execute("""SELECT first_name FROM user_account as ua, user_login as ul WHERE ua.user_id = ul.user_id AND user_name=%s""", (email,))
            name = cur.fetchone()
            cur.execute("""SELECT * FROM user_login WHERE user_name=%s""", (email,))
            account = cur.fetchone()
            cur.execute("""SELECT user_role FROM user_login WHERE user_name=%s""",(email,))
            db_role = cur.fetchone()
            print("role is ", db_role)

            if account:
                user = User(name, email, in_password, db_role[0])
                session['user-role'] = user.access
                return render_template('home.html', user=user)
    return render_template('login.html') # called when the request.method is not 'POST'

# may or may not implement this lol. not super important
@app.route('/logout', methods=['POST','GET'])
def logout():
    return
@app.get('/artworks')
def artworks():
        user = session["user-role"]
        return render_template('artworks.html', user=user)

@app.get('/exhibitions')
def exhibitions():
    return render_template('exhibitions.html')

@app.get('/films')
def films():
    return render_template('films.html')

@app.get('/members')
def members():
    return render_template('members.html')

@app.get('/gift_shop')
def gift_shop():
    return render_template('gift_shop.html')

@app.get('/employees')
def employees():
    return render_template('employees.html')

@app.get('/add_new_artwork')
def add_new_artwork():
    return render_template('add_new_artwork.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    msg = ""
    if request.method == 'POST':
       
        email = request.form['user_email']
        password = request.form['user_password']
        
# need to create page
@app.route('/user_info')
def user_info():
    f_name = request.form['user_fname']
    l_name = request.form['user_lname']
    # address area
    line_1 = request.form['line_1']
    city = request.form['city']
    state = request.form['state']
    phone_number = request.form['phone_number']
    sex = request.form['sex']
    dob = request.form['dob']
    temp.insert_user(cur,f_name,l_name,(line_1,city,state), phone_number,sex, dob, 'NONE')

@app.get('/report_gifts')
def report_gifts():
    # need to give range of data
    gift_name = request.args.get('gift-name')
    start_date = request.args.get('start-date')
    end_date = request.args.get('end-date')
    if gift_name and start_date and end_date:
        cur.execute("""
            SELECT i.gift_sku, i.gift_name, i.gift_price, DATE(s.gift_transaction_at)
            FROM gift_shop_item as i
            INNER JOIN gift_shop_sales as s 
            ON s.gift_sku = i.gift_sku 
            WHERE i.gift_name = %s AND DATE(s.gift_transaction_at) > %s AND DATE(s.gift_transaction_at) < %s """, [gift_name, start_date, end_date]
            )
        data = cur.fetchall()
        app.logger.info(data)
        return render_template('report_gifts.html', data=data)
    else:
        return render_template('report_gifts.html')
            
@app.get('/report_tickets')
def report_tickets():
    msg = ""
    start_date = request.args.get('start-date')
    end_date = request.args.get('end-date')
    if start_date and end_date:
        cur.execute("""
        SELECT exhib_title as event, exhib_ticket_price as ticket_price, DATE(exhib_transac_at)
        FROM exhibitions as e
            INNER JOIN exhib_ticket_sales as et ON e.exhib_id = et.exhib_id
        WHERE DATE(exhib_transac_at) >= %s AND DATE(exhib_transac_at) <= %s
        UNION
        SELECT film_title, film_ticket_price, DATE(film_transac_at)
        FROM films as f
            INNER JOIN film_ticket_sales as ft ON f.film_id = ft.film_id
        WHERE DATE(film_transac_at) >= %s AND DATE(film_transac_at) <= %s
        """, [start_date, end_date, start_date,end_date])
        data = cur.fetchall()
        app.logger.info(data)
        return render_template('report_tickets.html', data=data) # fill it in
    else:
        msg = "Invalid query. Please try again!"
        return render_template('report_tickets.html', msg=msg)


