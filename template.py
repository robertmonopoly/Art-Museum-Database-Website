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


def insert_user(cur, user_fname,user_lname, user_addr,p_number,user_sex, user_dob,membership):
    # generate uuid
    user_uuid = str(uuid.uuid4())
    result = cur.execute("""INSERT INTO user_account (user_id, first_name, last_name,user_address,email,phone_number, sex, date_of_birth, membership)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (user_uuid, user_fname,user_lname, user_addr, p_number, user_sex, user_dob,membership))
def insert_user_login(cur, user_role, user_name, pw, login_at ):
    # email is used as username
    user_uuid = cur.execute("""SELECT * FROM user_account WHERE email=?""", user_name)
    hashed = hash_pw(pw)
    result = cur.execute("""INSERT INTO user_login (user_id, user_role, user_name, hashed_password, login_at)
                            VALUES (?,?,?,?,?)""", (user_uuid,user_role, user_name, hashed, login_at))


# WARNING: the area below is all pseudo or unfinished code                     

def insert_art(cur, obj_num,title, artist, culture, made_on, obj_type, art_dpt, dim):
    return


def insert_gift_item(cur, gift_sku, gift_name, gift_type, gift_price):
    return


def insert_gift_sales(cur, transac_id, gift_sku, transac_at, user_id):
    return
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
