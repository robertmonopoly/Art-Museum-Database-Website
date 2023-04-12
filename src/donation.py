# import
import uuid
from datetime import date

def retrieve_donations_data(cur):
    cur.execute("""SELECT d.donation_transaction_id, u.first_name, u.last_name, 
    d.donator_email, d.donation_amount, u.membership, d.donation_on
    FROM donation as d
    INNER JOIN user_account as u
    ON d.donator_email = u.email
    GROUP BY d.donation_transaction_id, u.first_name, u.last_name, d.donator_email, u.membership, d.donation_on
    """)
    data = cur.fetchall()
    return data 

def retrieve_donation_sum(cur):
        cur.execute("""SELECT SUM(donation_amount)
        FROM donation""")
        data = cur.fetchone()
        return data

def insert_donation(cur, conn, email_address, money_amount):
    try:
        transac_id = str(uuid.uuid4())
        donation_date = date.today()
        cur.execute("INSERT INTO donation (donation_transaction_id, donator_email, donation_on, donation_amount) VALUES (%s, %s, %s, %s)", 
        (transac_id, email_address, donation_date, money_amount))
        conn.commit()
        print("Donation added successfully")
    except Exception as e:
        print(f"Error inserting donation: {e}")
