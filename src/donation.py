# import
import uuid
from datetime import date

def retrieve_donations_data(cur):
    cur.execute("""SELECT d.donation_transaction_id, u.first_name, u.last_name, 
    d.donator_email, d.donation_amount, u.membership, d.donation_on
    FROM donation as d
    INNER JOIN user_account as u
    ON d.donator_email = u.email
    """)
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
