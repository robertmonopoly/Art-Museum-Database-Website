# import
import uuid

from flask import request

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

def delete_film(cur, conn, film_id):
    try:
        cur.execute("DELETE FROM films WHERE film_id = %s", (film_id,))
        conn.commit()
        print("Film deleted successfully")
    except Exception as e:
        print("An error occurred while deleting the film", e)

def update_film(cur, conn, film_id, viewing_at, film_title, film_price, film_dur, film_dir, film_rate):
    try:
        cur.execute("""UPDATE films SET film_title = %s, viewing_at = %s, film_ticket_price = %s, duration_min = %s, film_director = %s, film_rating = %s WHERE film_id = %s""", (film_title, viewing_at, film_price, film_dur, film_dir, film_rate, film_id))
        conn.commit()
        print("Film updated successfully!")
    except Exception as e:
        print("An error occurred while updating the film:", e)

'''def insert_ticket_transaction(cur, conn, event_name, num_tickets, email):
  try:
    # this is how u do transaction id
    event_transac_id = str(uuid.uuid4())

    cur.execute("""SELECT user_id from user_account WHERE email = %s """, (email,))
    user_id = cur.fetchone()

    cur.execute("""SELECT film_ticket_price FROM films WHERE film_title = %s """, (event_name,))
    price_per_ticket = cur.fetchone()


    cur.execute("""SELECT film_id FROM films WHERE film_title = %s""", (event_name,))
    event_id = cur.fetchone()

    cur.execute("""INSERT INTO ticket_sales VALUES
    (%s, %s, %s, %s, %s)""",
    (event_transac_id, user_id, event_id, event_name, num_tickets))
    conn.commit()

    print("Film ticket transaction inserted successfully")
  except Exception as e:
    print("An error occurred while inserting the transaction", e)'''


def insert_ticket_transaction(cur, conn, event_name, num_tickets, email):
    try:
        # Generate a unique transaction ID
        event_transac_id = str(uuid.uuid4())

        # Get the user ID for the given email address
        cur.execute("""SELECT user_id FROM user_account WHERE email = %s""", (email,))
        user_id = cur.fetchone()[0]
        print(user_id)

        # Get the price per ticket for the given event name
        #cur.execute("""SELECT film_ticket_price FROM films WHERE film_title = %s""", (event_name,))
        #price_per_ticket = cur.fetchone()[0]
        
        # Get the event ID for the given event name
        cur.execute("""SELECT film_id FROM films WHERE film_title = %s""", (event_name,))
        event_id = cur.fetchone()[0]
        print(event_id)
        # Insert the ticket transaction into the database
        cur.execute("""INSERT INTO ticket_sales
                        VALUES (%s, %s, %s, %s, %s)""",
                    (event_transac_id, user_id, event_id, event_name, num_tickets))
        conn.commit()

        # Print a success message to the command line
        print("Ticket transaction inserted successfully")
    except Exception as e:
        print("An error occurred while inserting the transaction:", e)



def retrieve_ticket_data(cur):
    cur.execute("""SELECT * FROM ticket_sales""")
    data = cur.fetchall()
    return data    


