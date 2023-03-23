import uuid
import bcrypt

# need to create user class




# probably separate this function into a helper.py file
def hash_pw(password):
    # encoding user password
    bytes = password.encode('utf-8')
    # generating the salt
    salt = bcrypt.gensalt()
    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)
    print(hash)
    userBytes = password.encode('utf-8')
    # checking password (boolean)
    result = bcrypt.checkpw(userBytes, hash)
    # print(result)
    return result


@app.route('/registration', methods=['POST'])
def insert_user():
    # generate uuid
    user_uuid = str(uuid.uuid4())
    user_fname = request.form['user_fname']
    user_lname = request.form['user_lname']
    user_email = request.form['user_email']
    user_password = request.form['user_password']

   # insert user into database
    try:
        result = cur.execute("""INSERT INTO user_account (user_id, first_name, last_name, email, password)
                               VALUES (?, ?, ?, ?, ?)""", (user_uuid, user_fname, user_lname, user_email, user_password))
        db.commit()
        return 'User registered successfully!'
    except:
        db.rollback()
        return 'User registration failed.'


def insert_user_login(cur, user_role, user_name, pw, login_at ):
    # email is used as username
    user_uuid = cur.execute("""SELECT * FROM user_account WHERE email=?""", user_name)
    hashed = hash_pw(pw)
    result = cur.execute("""INSERT INTO user_login (user_id, user_role, user_name, hashed_password, login_at)
                            VALUES (?,?,?,?,?)""", (user_uuid,user_role, user_name, hashed, login_at))


# WARNING: the area below is all pseudo or unfinished code                     

def insert_art(cur, obj_num,title, artist, culture, made_on, obj_type, art_dpt, dim):
    sql_query = "INSERT INTO artworks (object_number, artwork_title, artist, culture, made_on, object_type, art_department, dimensions) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (obj_num, title, artist, culture, made_on, obj_type, art_dpt, dim)
    try:
        cur.execute(sql_query, values)
    except Exception as e:
        print(f"Error inserting values into artworks table: {e}")
    else:
        print("Values inserted successfully!")


def insert_gift_item(cur, gift_sku, gift_name, gift_type, gift_price):
    try:
        sql_query = "INSERT INTO gift_shop_item (gift_SKU, gift_name, gift_type, gift_price) VALUES (%s, %s, %s, %s);"
        cur.execute(sql_query, (gift_sku, gift_name, gift_type, gift_price))
    except Exception as e:
        return f"Error inserting gift item: {e}"
    else:
        return "Gift item inserted successfully."


def insert_gift_sales(cur, transac_id, gift_sku, transac_at, user_id):
    try:
        # Extract values from the request body
        gift_sku = request.json['gift_sku']
        transac_at = request.json['transaction_at']
        user_id = request.json['user_id']

        # Generate a unique transaction ID using the uuid4() function
        transac_id = uuid4()

        # Insert the values into the gift_shop_sales table
        sql = "INSERT INTO gift_shop_sales (gift_transaction_id, gift_SKU, gift_transaction_at, user_id) VALUES (%s, %s, %s, %s)"
        cur.execute(sql, (transac_id, gift_sku, transac_at, user_id))
        conn.commit()

        # Return a success message
        return jsonify({'message': 'Gift sale inserted successfully.'}), 201
    except Exception as e:
        # If any error occurs, rollback the transaction and return an error message
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        # Close the database connection
        cur.close()



# these (PSEUDO) functions require mapping
def get_all_events(conn):
    rs = conn.execute("SELECT * FROM events");
    if rs:
        #map(convert_row_to_event, rs)
        return
    else:
        # no results found
        return None
def get_user_by_id(cur, user_uuid):
    rs = cur.execute("SELECT * FROM users WHERE id=?", (user_uuid))
    if rs:
        # call mapper function here
        return 
    else:
        # no result found
        return None
