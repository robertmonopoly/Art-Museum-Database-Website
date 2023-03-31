# This file is just a library of SQL functions; no connection is actually being done here.
import uuid
import hash_password as hw

# User Class
class User():
    def __init__(self, name, email, password, access='USER'):
        self.name = name
        self.email = email
        self.password = password
        self.access = access
    
    def is_admin(self):
        return self.access == 'ADMIN'


# @app.route('/registration', methods=['POST']) -> use this when connecting db and routing html
def insert_user(cur, user_fname,user_lname, user_addr,p_number,user_sex, user_dob,membership):
    # generate uuid
    user_uuid = str(uuid.uuid4())
   # insert user into database
    cur.execute("""INSERT INTO user_account VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (user_uuid, user_fname,user_lname, user_addr, p_number, user_sex, user_dob,membership))

def insert_user_login(cur, user_role, user_name, pw, login_at ):
    # email is used as username
    user_uuid = cur.execute("""SELECT * FROM user_account WHERE email=?""", user_name)
    hashed = hw.hash_pw(pw)
    cur.execute("""INSERT INTO user_login VALUES (%s, %s, %s, %s, %s)""", (user_uuid,user_role, user_name, hashed, login_at))
    
    # note: this part is completely separate from this function; we will use it when connecting to db!
    # try:
        # call the insert_user_login function!
    #     insert_user_login(cur, user_name, user_password, login_at)
    #     cur.commit()
    #     return 'User registered successfully!'
    # except:
    #     cur.rollback()
    #     return 'User registration failed.'
                   
# report functions
def insert_gift_rep(cur, g_name, s_date, e_date):
    cur.execute("""
    SELECT i.gift_sku, i.gift_name, i.gift_price, DATE(s.gift_transaction_at)
    FROM gift_shop_item as i
    INNER JOIN gift_shop_sales as s 
    ON s.gift_sku = i.gift_sku 
    WHERE i.gift_name = %s AND DATE(s.gift_transaction_at) >= %s AND DATE(s.gift_transaction_at) <= %s """, [g_name, s_date, e_date]
    )
    data = cur.fetchall()
    return data

def insert_ticket_rep(cur, s_date,e_date):
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
        """, [s_date, e_date, s_date,e_date])
    data = cur.fetchall()
    return data

def insert_member_don(cur):
    return

# end report functions

# insert functions
def insert_art(cur, artist, title, made_on, obj_type, obj_num, art_byte):
    sql_query = """INSERT INTO artworks VALUES (%s, %s, %s, %s, %s, %s)"""
    values = (artist,title, made_on, obj_type, obj_num, art_byte)
    try:
        cur.execute(sql_query, values)
        data = cur.fetchall()
        cur.commit()
        print("Art values inserted successfully!")
        return data
    except Exception as e:
        print(f"Error inserting values into artworks table: {e}")
   
def insert_gift_item(cur, gift_sku, gift_name, gift_type, gift_price):
    sql_query = """INSERT INTO gift_shop_item VALUES (%s, %s, %s, %s)"""
    values = (gift_sku, gift_name, gift_type, gift_price)
    try:
        cur.execute(sql_query,values)
        data = cur.fetchall()
        cur.commit()
        print("Gift item inserted successfully.") 
        return data
    except Exception as e:
        print (f"Error inserting gift item: {e}")
   

def insert_gift_sales(cur, transac_id, gift_sku, transac_at, user_id):
    try:
        # Extract values from the request body -> do this in login.py file
        # gift_sku = request.json['gift_sku']
        # transac_at = request.json['transaction_at']
        # user_id = request.json['user_id']

        # Generate a unique transaction ID using the uuid4() function
        transac_id = str(uuid.uuid4())

        # Insert the values into the gift_shop_sales table
        sql = "INSERT INTO gift_shop_sales VALUES (%s, %s, %s, %s)"
        try:
            cur.execute(sql, (transac_id, gift_sku, transac_at, user_id))
      
        except Exception as e:
            print(f"Error inserting values into gift table: {e}")
        else:
            print("Values inserted successfully!")
        cur.commit()

        
    except Exception as e:
        # If any error occurs, rollback the transaction and return an error message
        cur.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        # Close the database connection
        cur.close()



def insert_exhibition(cur, exhib_id, exhib_at, exhib_price, exhib_gallery, exhib_title, exhib_curator):
    try:
        cur.execute("""INSERT INTO exhibitions VALUES (%s, %s, %s, %s, %s, %s)""", (exhib_id, exhib_at, exhib_price, exhib_gallery, exhib_title, exhib_curator))
    except Exception as e:
        print("An error occurred while inserting the exhibition:", e)


def insert_exhib_sales(cur, exhib_transac_id, user_id, exhib_id, exhib_transac_at):
    try:
        cur.execute("""INSERT INTO exhibition_ticket_sales VALUES(%s, %s, %s, %s)""", (exhib_transac_id, user_id, exhib_id, exhib_transac_at))
    except Exception as e:
        print("An error occurred while inserting the exhibition sales record:", e)

# ALERT: might change film_rate to an ENUM of value 1-5 stars!!!!!!!!!!!!!!
def insert_films(cur,film_id, film_title, film_price, film_dur, film_dir, film_rate):
    cur.execute("""INSERT INTO films VALUES (%s, %s, %s, %s, %s, %s)""", (film_id, film_title, film_price, film_dur, film_dir, film_rate))

def insert_film_sales(cur, film_transac_id, user_id, film_id, film_transac_at):
    try:
        cur.execute("""INSERT INTO film_ticket_sales VALUES (%s, %s, %s, %s, %s)""", (film_transac_id, user_id, film_id, film_transac_at))
    except Exception as e:
        print("An error occurred while inserting the film sales record:", e)

def delete_artwork(cur, obj_num):
    try:
        cur.execute("DELETE * FROM artworks WHERE obj_num = artworks.obj_num")
    except Exception as e:
        print("An error occurred while deleting the artwork", e)

def delete_film(cur, film_id):
    try:
        cur.execute("DELETE * FROM films WHERE film_id = films.film_id")
    except Exception as e:
        print("An error occurred while deleting the film", e)

def delete_employee(cur, employee_id):
    try:
        cur.execute("DELETE * FROM artworks WHERE employee_id = employees.employee_id")
    except Exception as e:
        print("An error occurred while deleting the employee's records", e)    

def delete_gift_shop_item(cur, gift_sku):
    try:
        cur.execute("DELETE * FROM gift_shop_item WHERE gift_sku = gift_shop_item.gift_sku")
    except Exception as e:
        print("An error occurred while deleting the item", e)

def delete_exhibit(cur, exhib_id):
    try:
        cur.execute("DELETE * FROM exhibitions WHERE exhib_id = exhibitions.exhib_id")
    except Exception as e:
        print("An error occurred while deleting the exhibit", e)  

# these (PSEUDO) functions require mapping
def get_all_events(conn):
    rs = conn.execute("SELECT * FROM events")
    events = []
    for row in event_table:
        event = convert_row_to_event(row)
        events.append(event)
    return events

def get_user_by_id(cur, user_uuid):
    rs = cur.execute("SELECT * FROM users WHERE id=?", (user_uuid))
    if rs:
        # call mapper function here
        return 
    else:
        # no result found
        return None
