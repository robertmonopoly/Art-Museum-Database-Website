from flask import Flask, request, render_template, make_response, redirect, url_for, session
import psycopg2
import template as temp
import hash_password as hp
app = Flask(__name__)
app.secret_key = 'my_secret'

# Local Connection
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
    
@app.route('/signup', methods=['POST','GET'])
def signup():
    msg = ""
    if request.method == 'POST':
        email = request.form['user_email']
        password = request.form['user_password']

@app.route('/login', methods =['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['user_email'] 
        in_password = request.form['user_password']
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
                user = temp.User(name, email, in_password, db_role[0])
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

@app.get('/add_new_exhibition')
def add_new_exhibition():
    return render_template('add_new_exhibition.html')

@app.get('/add_new_film')
def add_new_film():
    return render_template('add_new_film.html')

@app.get('/add_new_employee')
def add_new_employee():
    return render_template('add_new_employee.html')

@app.get('/add_new_member')
def add_new_member():
    return render_template('add_new_member.html')

@app.get('/add_new_artwork')
def add_new_artwork():
    return render_template('add_new_artwork.html')

@app.get('/add_new_gift_shop_item')
def add_new_gift_shop_item():
    return render_template('add_new_gift_shop_item.html')

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

@app.get('/Eticket_details')
def Eticket_details():
    return render_template('Eticket_details')

@app.get('/Fticket_details')
def Fticket_details():
    return render_template('Fticket_details')


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
    mgs = ""
    gift_name = request.args.get('gift-name')
    start_date = request.args.get('start-date')
    end_date = request.args.get('end-date')
    if gift_name and start_date and end_date:
        data = temp.insert_gift_rep(cur, gift_name,start_date,end_date)
        if data == []:
            msg = "There was no report for the selected interval. Please try another set of dates!"
            return render_template('report_gifts.html', msg=msg)
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
        data = temp.insert_ticket_rep(cur, start_date, end_date)
        if data == []:
            msg = "There was no report for the selected interval. Please try another set of dates!"
            return render_template('report_tickets.html', msg=msg)
        app.logger.info(data)
        return render_template('report_tickets.html', data=data) # fill it in
    else:
        return render_template('report_tickets.html')


