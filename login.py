from flask import Flask, request, render_template, make_response, redirect, url_for, session, flash
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import uuid
import query as q
import hash_password as hp
#import PIL.Image as Image

from io import BytesIO
app = Flask(__name__)
app.secret_key = 'my_secret'


# Local Connection
try:
    with open("config.toml") as tomlfile:
        content = tomlfile.read()
    conn = psycopg2.connect(content)
    cur = conn.cursor()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    print("Connected to Postgres")
except Exception as e:
    print("An error occurred while connecting: ", e)


try:
    # Create the trigger function
    cur.execute("""
        CREATE OR REPLACE FUNCTION display_message() RETURNS TRIGGER AS 
        $$
        BEGIN
            RAISE NOTICE 'An exhibition or film has been inserted into the database.';
            RAISE NOTICE 'Trigger function called successfully';
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Create the trigger for exhibitions
    cur.execute("""
        CREATE TRIGGER insert_exhibition_trigger
        AFTER INSERT ON exhibitions
        FOR EACH ROW
        EXECUTE FUNCTION display_message();
    """)

    # Create the trigger for films
    cur.execute("""
        CREATE TRIGGER insert_films_trigger
        AFTER INSERT ON films
        FOR EACH ROW
        EXECUTE FUNCTION display_message();
    """)
    conn.commit()
    print("Triggers created successfully")
except Exception as e:
    print("An error occurred while creating the triggers:", e)



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
    return render_template("signup.html")

@app.route('/registration', methods=['POST','GET'])
def registration():
    msg = ""
    if request.method == 'POST':
        email = request.form['user_email']
        password = request.form['user_password']
    return render_template("registration.html")

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
            # db_role is printed out as a tuple
            db_role = cur.fetchone()
            print("role is ", db_role[0])

            if account:
                user = q.User(name, email, in_password, db_role[0])
                session['user-role'] = user.access
                return redirect(url_for('home'))
    return render_template('home.html') # called when the request.method is not 'POST'

# hmm, i tried to complete this function for u guys, it is probably close to
# complete, but we would need a logout button, maybe it could be on the navbar
# or on the top right of our webpages - sincerely, monopoly
@app.route('/logout', methods=['POST','GET'])
def logout():
    session.clear()
    return render_template(url_for('login.html'))

@app.get('/artworks')
def artworks():
        user = session["user-role"]
        return render_template('artworks.html', user=user)

#TODO: now do image upload
#TODO: remember to pass in the connector for SQL commits
@app.route('/add_new_artwork', methods=['POST','GET'])
def add_new_artwork():
    if request.method == 'POST':
        artist = request.form['artist']
        title = request.form['artwork_title']
        made_on = request.form['made_on']
        obj_type = request.form['object_type']
        obj_num = request.form['object_number']
        art_file = request.files['art_img']
 
       # Convert image to bytes
        pil_im = Image.open(art_file, mode = 'r')
        border = (20, 20, 100, 100)
        cropped = pil_im.crop(border)
        b = BytesIO()

        cropped.save(b, 'jpeg')
        im_bytes = b.getvalue()
        #print("my bytes ", im_bytes)

        q.insert_art(cur, conn, artist,title,made_on, obj_type, obj_num, im_bytes)
        # after insert, send to artworks page and then update page by calling the latest query from the artworks table and pass it into macro template
    return render_template('add_new_artwork.html')
  

@app.route('/update_artwork', methods=['POST','GET'])
def update_artwork():
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
        data = q.update_art(cur,artist,title,made_on, obj_type, obj_num, im_bytes)
        return render_template('add_new_artwork.html', data=data)
    else:
        return render_template('add_new_artwork.html')


@app.get('/donations')
def donations():
    user = user = session["user-role"]
    return render_template('donations.html', user=user)

@app.route('/add_new_donation', methods = ['GET', 'POST'])
def add_new_donation():
    if request.method == 'POST':
        first_name = request.form['f_name']
        last_name = request.form['l_name']
        email_address = request.form['email']
        money_amount = request.form['donation_amount']
        data = q.insert_donation(cur, conn, first_name, last_name,
        email_address, money_amount)
        return render_template('donations.html')
    else:
        return render_template('donations.html')
    
@app.get('/exhibitions')
def exhibitions():
    user = user = session["user-role"]
    return render_template('exhibitions.html', user=user)

@app.route('/add_new_exhibition', methods = ['GET', 'POST'])
def add_new_exhibition():
    if request.method == 'POST':
       
        date_and_time = request.form['exhibition_at']
        ticket_price = request.form['exhibition_ticket_price']
        gallery = request.form['exhibition_gallery']
        title = request.form['exhibition_title']
        curator = request.form['curator']
        artists = request.form['exhibition_artists']
        data = q.insert_exhibition(cur, conn, date_and_time, ticket_price,
        gallery, title, curator, artists)
        return render_template('add_new_exhibition.html')
    else:
        return render_template('add_new_exhibition.html')

@app.route('/update_exhibition', methods = ['POST'])
def update_exhibition():
    if request.method == 'POST':
        exhibit_id = request.form['exhibition_id']
        date_and_time = request.form['exhibition_at']
        ticket_price = request.form['exhibition_ticket_price']
        gallery = request.form['exhibition_gallery']
        title = request.form['exhibition_title']
        curator = request.form['curator']
        artists = request.form['exhibition_artists']
        try:
            data = q.update_exhibition(cur, conn, exhibit_id, date_and_time, ticket_price,
        gallery, title, curator, artists)
            flash('Exhibition updated successfully.')
        except Exception as e:
            print(f"Error updating exhibition: {e}")
            flash('Error updating exhibition.')
        return render_template('add_new_exhibition.html')
    else:
        return render_template('add_new_exhibition.html')

@app.route('/delete_exhibition', methods = ['POST'])
def delete_exhibition():
    if request.method == 'POST':
        exhibit_id = request.form['exhibition_id']
        try:
            data = q.delete_exhibit(cur, conn, exhibit_id)
        except Exception as e:
            print(f"Error deleting exhibition: {e}")
            flash('Error deleting exhibition.')
        return render_template('add_new_exhibition.html')

@app.route('/add_new_film', methods=['GET', 'POST'])
def add_new_film():
    if request.method == 'POST':
        location = request.form['viewing_at']
        title = request.form['film_title']
        ticket_price = request.form['film_ticket_price']
        duration = request.form['duration_min']
        director = request.form['film_director']
        rating = request.form['film_rating']
        data = q.insert_films(cur, conn, location,
        title, ticket_price, duration, director,
        rating)
        return render_template('add_new_film.html')
    else:
        return render_template('add_new_film.html')

@app.route('/update_film', methods = ['POST'])
def update_film():
    if request.method == 'POST':
        num_id = request.form['film_id']
        location = request.form['viewing_at']
        title = request.form['film_title']
        ticket_price = request.form['film_ticket_price']
        duration = request.form['duration_min']
        director = request.form['film_director']
        rating = request.form['film_rating']
        data = q.update_film(cur, conn, num_id, location,
        title, ticket_price, duration, director,
        rating)
        return render_template('add_new_film.html')
    else:
        return render_template('add_new_film.html')


@app.route('/delete_film', methods = ['POST'])
def delete_film():
    num_id = request.form['film_id']
    try:
        q.delete_film(cur, conn, num_id)
        flash('Film deleted successfully')
    except Exception as e:
        print (f"Error deleting film: {e}")
        flash('Error deleting film.')
    return render_template('add_new_film.html') 

@app.route('/add_new_employee', methods=['GET', 'POST'])
def add_new_employee():
    if request.method == 'POST':
        membership = request.form['membership']
        first_name = request.form['employee_first_name']
        last_name = request.form['employee_last_name']       
        email = request.form['employee_email']
        ssn = request.form['employee_ssn']
        phone_number = request.form['employee_phone_number']
        dob = request.form['employee_date_of_birth']
        salary = request.form['salary']
        q.insert_employee(cur, conn, membership, first_name,
        last_name, email, ssn, phone_number,
        dob, salary)
    return render_template('add_new_employee.html')
    

@app.route('/update_employee', methods = ['POST'])
def update_employee():
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
        data = q.update_employee(cur, membership, first_name,
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
        data = q.insert_member(cur, conn, first_name, last_name,
        address_line1, address_line2, city, state,
        zip_code, email, phone_number, gender, dob, membership_type)
        return render_template('add_new_member.html')
    else:
        return render_template('add_new_member.html')

@app.route('/update_member', methods = ['POST'])
def update_member():
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
        data = q.update_member(cur, conn, first_name, last_name,
        address_line1, address_line2, city, state,
        zip_code, email, phone_number, gender, dob, membership_type)
        return render_template('add_new_member.html')
    else:
        return render_template('add_new_member.html')

@app.route('/delete_member', methods = ['POST'])
def delete_member():        
    if request.method == 'POST':
        member_id = request.form['account_id']
        try:
            q.delete_member(cur, conn, member_id)
            flash('User account deleted successfully')
        except Exception as e:
            print(f"Error deleting user account: {e}")
            flash('Error deleting user account.')
    return render_template('add_new_member.html')

@app.route('/add_new_gift_shop_item', methods=['GET', 'POST'])
def add_new_gift_shop_item():
    if request.method == 'POST':
        name = request.form['name']
        item_type = request.form['type']
        price = request.form['price']
        try:
            q.insert_gift_item(cur, conn, name, item_type, price)
            flash('Gift item added successfully.')
        except Exception as e:
            print(f"Error adding gift item: {e}")
            flash('Error adding gift item.')
    return render_template('add_new_gift_shop_item.html')

@app.route('/update_gift_shop_item', methods=['POST'])
def update_gift_shop_item():
    gift_sku = request.form['sku']
    gift_name = request.form['name']
    gift_type = request.form['type']
    gift_price = request.form['price']
    try:
        q.update_gift_item(cur, conn, gift_sku, gift_name, gift_type, gift_price)
        flash('Gift item updated successfully.')
    except Exception as e:
        print (f"Error updating gift item: {e}")
        flash('Error updating gift item.')
    return render_template('add_new_gift_shop_item.html')


@app.route('/delete_gift_shop_item', methods=['POST'])
def delete_gift_shop_item():
    gift_sku = request.form['sku']
    try:
        q.delete_gift_shop_item(cur, conn, gift_sku)
        flash('Gift item deleted successfully')
    except Exception as e:
        print (f"Error deleting gift item: {e}")
        flash('Error deleting gift item.')
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

