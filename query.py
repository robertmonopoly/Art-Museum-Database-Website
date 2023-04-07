# This file is just a library of SQL functions; no connection is actually being done here.
import uuid
import hash_password as hw
from datetime import date

# User Class
class User():
    def __init__(self, name, email, password, access='USER'):
        self.name = name
        self.email = email
        self.password = password
        self.access = access
    
    def is_admin(self):
        return self.access == 'ADMIN'


def insert_user(cur, conn, user_fname, user_lname, user_email, user_dob):
    # generate uuid
    user_uuid = str(uuid.uuid4())
    active_account = 1
    membership_lvl = "NONE"
   # insert user into database
    try:
        cur.execute("""INSERT INTO user_account VALUES (%s, %s, %s, %s, %s, %s, %s)""", (user_uuid, user_fname, user_lname, user_email, user_dob, membership_lvl, active_account))
        conn.commit()
        print("user successfully inserted")
    except Exception as e:
        print("There was an error creating the account:", {e})

def insert_user_login(cur, conn, user_role, user_name, pw, login_at ):
    # email is used as username
    user_uuid = cur.execute("""SELECT * FROM user_account WHERE email=?""", user_name)
    hashed = hw.hash_pw(pw)
    cur.execute("""INSERT INTO user_login VALUES (%s, %s, %s, %s, %s)""", (user_uuid,user_role, user_name, hashed, login_at))
    
                   
# report functions
def insert_gift_rep(cur, g_name, s_date, e_date):
    cur.execute("""
    SELECT i.gift_sku, i.gift_name, i.gift_price, DATE(s.gift_transaction_at)
    FROM gift_shop_item as i
    INNER JOIN gift_shop_sales as s 
    ON s.gift_sku = i.gift_sku 
    WHERE i.gift_name = %s AND DATE(s.gift_transaction_at) >= %s AND DATE(s.gift_transaction_at) <= %s """, [g_name, s_date, e_date]
    )
    data = cur.fetchall() # is THERE NO NEED TO FETCH WHEN UR INSERTING VALS?
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
def insert_art(cur, conn, artist, title, made_on, obj_type, obj_num, art_byte):
    sql_query = """INSERT INTO artworks VALUES (%s, %s, %s, %s, %s, %s)"""
    values = (artist,title, made_on, obj_type, obj_num, art_byte)
    try:
        cur.execute(sql_query, values)
        print("Art values inserted successfully!")
        conn.commit() # VERY IMPORTANT because of sql transactions
    except Exception as e:
        print(f"Error inserting values into artworks table: {e}")
   
def insert_gift_item(cur, conn, gift_name, gift_type, gift_price):
    try:
        gift_sku = str(uuid.uuid4())
        sql_query = """INSERT INTO gift_shop_item VALUES (%s, %s, %s, %s)"""
        values = (gift_sku, gift_name, gift_type, gift_price)
        cur.execute(sql_query,values)
        conn.commit()
        print("Gift item inserted successfully.") 
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
        #return jsonify({'error': str(e)}), 400
    finally:
        # Close the database connection
        cur.close()



def insert_donation(cur, conn, first_name, last_name, email_address, money_amount):
    try:
        transac_id = str(uuid.uuid4())
        donation_date = date.today()
        cur.execute("INSERT INTO donation (donation_transaction_id, donator_first_name, donator_last_name, donator_email, donation_on, donation_amount) VALUES (%s, %s, %s, %s, %s, %s)", 
        (transac_id, first_name, last_name, email_address, donation_date, money_amount))
        conn.commit()
        print("Donation added successfully")
    except Exception as e:
        print(f"Error inserting donation: {e}")



def insert_exhibition(cur, conn, exhib_at, exhib_price, exhib_gallery, exhib_title, exhib_curator, exhibition_artists):
    try:
        exhib_id = str(uuid.uuid4())
        cur.execute("""INSERT INTO exhibitions VALUES (%s, %s, %s, %s, %s, %s, %s)""", (exhib_id, exhib_at, exhib_price, exhib_gallery, exhib_title, exhib_curator, exhibition_artists))
        conn.commit()
        print("Exhibition inserted sucessfully")
    except Exception as e:
        print("An error occurred while inserting the exhibition:", e)


def insert_exhib_sales(cur, exhib_transac_id, user_id, exhib_id, exhib_transac_at):
    try:
        cur.execute("""INSERT INTO exhibition_ticket_sales VALUES(%s, %s, %s, %s)""", (exhib_transac_id, user_id, exhib_id, exhib_transac_at))
    except Exception as e:
        print("An error occurred while inserting the exhibition sales record:", e)

# ALERT: might change film_rate to an ENUM of value 1-5 stars!!!!!!!!!!!!!!
def insert_films(cur, conn, viewing_at, film_title, film_price, film_dur, film_dir, film_rate):
    try:
        film_id = str(uuid.uuid4())
        cur.execute("""INSERT INTO films (film_id, viewing_at, film_title, film_ticket_price, duration_min, film_director, film_rating)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (film_id, viewing_at, film_title, film_price, film_dur, film_dir, film_rate))
        conn.commit()
        print("Film inserted successfully")
    except Exception as e:
        print("An error occurred while inserting the film", e)

def insert_employee(cur, conn, membership, first_name, last_name, email, ssn, phone_number, dob, salary):
    employee_id = str(uuid.uuid4())
    query = """
        INSERT INTO employees (employee_id, employee_membership, employee_first_name, employee_last_name, employee_email, employee_ssn, employee_phone_number, employee_date_of_birth, salary)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cur.execute(query, (employee_id, membership, first_name, last_name, email, ssn, phone_number, dob, salary))
        conn.commit()
        print("New employee added successfully")
    except Exception as e:
        print("An error occurred while adding the new employee: ", e)


def insert_film_sales(cur, film_transac_id, user_id, film_id, film_transac_at):
    try:
        cur.execute("""INSERT INTO film_ticket_sales VALUES (%s, %s, %s, %s, %s)""", (film_transac_id, user_id, film_id, film_transac_at))
    except Exception as e:
        print("An error occurred while inserting the film sales record:", e)


def delete_artwork(cur, conn, obj_num):
    try:
        cur.execute("DELETE FROM artworks WHERE obj_num = ?", (obj_num,))
        conn.commit()
    except Exception as e:
        print("An error occurred while deleting the artwork", e)


def delete_member(cur, conn, user_account_id):
    try:
        cur.execute("UPDATE user_account SET account_status = %s WHERE user_id = %s", 
            (0, user_account_id))
        conn.commit()
        print("User account deleted successfully")
    except Exception as e:
        print("An error occurred while deleting the user account: ", e)

def delete_film(cur, conn, film_id):
    try:
        cur.execute("DELETE FROM films WHERE film_id = %s", (film_id,))
        conn.commit()
        print("Film deleted successfully")
    except Exception as e:
        print("An error occurred while deleting the film", e)

def delete_employee(cur, employee_id):
    try:
        cur.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
    except Exception as e:
        print("An error occurred while deleting the employee's records", e)    

def delete_gift_shop_item(cur, conn, gift_sku):
    try:
        cur.execute("DELETE FROM gift_shop_item WHERE gift_sku = %s", (gift_sku,))
        conn.commit()
        print("Item deleted successfully")
    except Exception as e:
        print("An error occurred while deleting the item", e)

def delete_exhibit(cur, conn, exhib_id):
    try:
        cur.execute("DELETE FROM exhibitions WHERE exhib_id = %s", (exhib_id,))
        conn.commit()
        print("Exhibit deleted successfully")
    except Exception as e:
        print("An error occurred while deleting the exhibit", e)
 


def update_art(cur, conn, artist, title, made_on, obj_type, obj_num, art_byte, art_id):
    sql_query = """UPDATE artworks SET artist = %s, title = %s, made_on = %s, obj_type = %s, obj_num = %s, art_byte = %s WHERE id = %s"""
    values = (artist, title, made_on, obj_type, obj_num, art_byte, art_id)
    try:
        cur.execute(sql_query, values)
        conn.commit()
        print("Art values updated successfully!")
      
    except Exception as e:
        print(f"Error updating values in artworks table: {e}")

def update_gift_item(cur, conn, gift_sku, gift_name, gift_type, gift_price):
    sql_query = """UPDATE gift_shop_item SET gift_name = %s, gift_type = %s, gift_price = %s WHERE gift_SKU = %s"""
    values = (gift_name, gift_type, gift_price, gift_sku)
    try:
        cur.execute(sql_query,values)
        conn.commit()
        print("Gift item updated successfully.")
    except Exception as e:
        print (f"Error updating gift item: {e}")


def update_exhibition(cur, conn, exhibition_id, exhib_at, exhib_price, exhib_gallery, exhib_title, exhib_curator, exhibition_artists):
    try:
        cur.execute("""UPDATE exhibitions SET exhib_at = %s, exhib_ticket_price = %s, exhib_gallery = %s, exhib_title = %s, curator = %s, exhib_artists = %s WHERE exhib_id = %s""",
         (exhib_at, exhib_price, exhib_gallery, exhib_title, exhib_curator, exhibition_artists, exhibition_id))
        conn.commit()
        print("Exhibition updated successfully!")
    except Exception as e:
        print("An error occurred while updating the exhibition:", e)
       

def update_film(cur, conn, film_id, viewing_at, film_title, film_price, film_dur, film_dir, film_rate):
    try:
        cur.execute("""UPDATE films SET film_title = %s, viewing_at = %s, film_ticket_price = %s, duration_min = %s, film_director = %s, film_rating = %s WHERE film_id = %s""", (film_title, viewing_at, film_price, film_dur, film_dir, film_rate, film_id))
        conn.commit()
        print("Film updated successfully!")
    except Exception as e:
        print("An error occurred while updating the film:", e)


# these (PSEUDO) functions require mapping
# def get_all_events(conn):
#     rs = conn.execute("SELECT * FROM events")
#     events = []
#     for row in event_table:
#         event = convert_row_to_event(row)
#         events.append(event)
#     return events

# def get_user_by_id(cur, user_uuid):
#     rs = cur.execute("SELECT * FROM users WHERE id=?", (user_uuid))
#     if rs:
#         # call mapper function here
#         return 
#     else:
#         # no result found
#         return None
