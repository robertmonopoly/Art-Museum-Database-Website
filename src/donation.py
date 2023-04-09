# import
import uuid
from datetime import date

def retrieve_donations_data(cur):
    cur.execute("""SELECT * FROM donation""")
    data = cur.fetchall()
    return data 

def insert_member_don(cur):
    return

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
