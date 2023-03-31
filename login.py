from flask import Flask, request, render_template, make_response, redirect, url_for, session
import psycopg2
import query as q
import hash_password as hp
# import PIL.Image as Image
from io import BytesIO
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
        user = session["user-role"]
        return render_template("home.html", user=user)
    
#TODO: setup registration page
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
                user = q.User(name, email, in_password, db_role[0])
                session['user-role'] = user.access
                return render_template('home.html', user=user)
    return render_template('login.html') # called when the request.method is not 'POST'

# may or may not implement this lol. not super important

# hmm, i tried to complete this function for u guys, it is probably close to
# complete, but we would need a logout button, maybe it could be on the navbar
# or on the top right of our webpages - sincerely, monopoly
@app.route('/logout', methods=['POST','GET'])
def logout():
    session.clear()
    return redirect(url_for('login.html'))

@app.get('/artworks')
def artworks():
        user = session["user-role"]
        return render_template('artworks.html', user=user)

#TODO: need to add new artwork
@app.route('/add_new_artwork', methods=['POST','GET'])
def add_new_artwork():
    if request.method == 'POST':
        artist = request.form['artist']
        title = request.form['artwork_title']
        made_on = request.form['made_on']
        obj_type = request.form['object_type']
        obj_num = request.form['object_number']
        upload_art = request.form['art_img']

        # Convert image to bytes
        pil_im = Image.fromarray(upload_art)
        b = BytesIO()
        pil_im.save(b, 'jpeg')
        im_bytes = b.getvalue()
        # read_art = upload_art.read()
        # byte_art = bytearray(read_art)
        # print("art in byte ", byte_art)
        data = q.insert_art(cur,artist,title,made_on, obj_type, obj_num, im_bytes)
        return render_template('add_new_artwork.html', data=data)
    else:
        return render_template('add_new_artwork.html')
    
@app.get('/exhibitions')
def exhibitions():
    user = user = session["user-role"]
    return render_template('exhibitions.html', user=user)

@app.get('/add_new_exhibition')
def add_new_exhibition():
    if request.method == 'POST':
        date_and_time = request.form['exhibition_at']
        ticket_price = request.form['exhibition_ticket_price']
        gallery = request.form['exhibition_gallery']
        title = request.form['exhibition_title']
        curator = request.form['curator']
        artists = request.form['exhibition_artists']
        data = q.insert_art(cur, date_and_time, ticket_price,
        gallery, title, curator, artists)
        return render_template('add_new_exhibition.html')
    else:
        return render_template('add_new_exhibition.html')

@app.get('/add_new_film')
def add_new_film():
    if request.method == 'POST':
        num_id = request.form['film_id']
        location = request.form['viewing_at']
        title = request.form['film_title']
        ticket_price = request.form['film_ticket_price']
        duration = request.form['duration_min']
        director = request.form['film_director']
        rating = request.form['film_rating']
        data = q.insert_art(cur, num_id, location,
        title, ticket_price, duration, director,
        rating)
        return render_template('add_new_film.html')
    else:
        return render_template('add_new_film.html')

@app.get('/add_new_employee')
def add_new_employee():
    if request.method == 'POST':
        membership = request.form['membership']
        first_name = request.form['employee_first_name']
        last_name = request.form['employee_last_name']
        address = request.form['employee_address']
        email = request.form['employee_email']
        ssn = request.form['employee_ssn']
        phone_number = request.form['employee_phone_number']
        dob = request.form['employee_date_of_birth']
        salary = request.form['salary']
        data = q.insert_art(cur, membership, first_name,
        last_name, address, email, ssn, phone_number,
        dob, salary)
        return render_template('add_new_employee.html')
    else:
        return render_template('add_new_employee.html')


@app.get('/add_new_member')
def add_new_member():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address_line1 = request.form['address_line1']
        address_line2 = request.form['address_line2']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip']
        email = request.form['email']
        phone_number = request.form['phone_number']
        gender = request.form['gender']
        dob = request.form['dob']
        membership_type = request.form['membership']
        data = q.insert_art(cur, first_name, last_name,
        address_line1, address_line2, city, state,
        zip_code, email, phone_number, gender, dob, membership_type)
        return render_template('add_new_member.html')
    else:
        return render_template('add_new_member.html')

@app.get('/add_new_gift_shop_item')
def add_new_gift_shop_item():
    if request.method == 'POST':
        sku = request.form['film_id']
        name = request.form['viewing_at']
        item_type = request.form['film_title']
        price = request.form['film_ticket_price']
        return render_template('add_new_gift_shop_item.html')
    else:
        return render_template('add_new_gift_shop_item.html')

@app.get('/films')
def films():
    user = session["user-role"]
    return render_template('films.html',user=user)

@app.get('/members')
def members():
    user = session["user-role"]
    return render_template('members.html',user=user)

@app.get('/gift_shop')
def gift_shop():
    user = session["user-role"]
    return render_template('gift_shop.html', user=user)

@app.get('/employees')
def employees():
    user = session["user-role"]
    return render_template('employees.html', user=user)

@app.get('/Eticket_details')
def Eticket_details():
    return render_template('Eticket_details')

@app.get('/Fticket_details')
def Fticket_details():
    return render_template('Fticket_details')


# TODO: need to create page
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
    q.insert_user(cur,f_name,l_name,(line_1,city,state), phone_number,sex, dob, 'NONE')

# the reports
@app.get('/report_gifts')
def report_gifts():
    mgs = ""
    gift_name = request.args.get('gift-name')
    start_date = request.args.get('start-date')
    end_date = request.args.get('end-date')
    if gift_name and start_date and end_date:
        data = q.insert_gift_rep(cur, gift_name, start_date, end_date)
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
        data = q.insert_ticket_rep(cur, start_date, end_date)
        if data == []:
            msg = "There was no report for the selected interval. Please try another set of dates!"
            return render_template('report_tickets.html', msg=msg)
        app.logger.info(data)
        return render_template('report_tickets.html', data=data) # fill it in
    else:
        return render_template('report_tickets.html')

# TODO: need to make third report

