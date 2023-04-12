#import 
import uuid

def insert_exhibition(cur, conn, exhib_at, exhib_price, exhib_gallery, exhib_title, exhib_curator, exhibition_artists):
    try:
        exhib_id = str(uuid.uuid4())
        cur.execute("""INSERT INTO exhibitions VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *""", 
                    (exhib_id, exhib_at, exhib_price, exhib_gallery, exhib_title, exhib_curator, exhibition_artists))
        conn.commit()
        print("Exhibition inserted successfully")
    except Exception as e:
        print("An error occurred while inserting the exhibition:", e)
        
        # Catch the exception raised by the trigger and print the message to the command line
        if "Trigger function failed" in str(e):
            print("An exhibition or film has been inserted into the database.")
            print("Trigger function called successfully")

def update_exhibition(cur, conn, exhibition_id, exhib_at, exhib_price, exhib_gallery, exhib_title, exhib_curator, exhibition_artists):
    try:
        cur.execute("""UPDATE exhibitions SET exhib_at = %s, exhib_ticket_price = %s, exhib_gallery = %s, exhib_title = %s, curator = %s, exhib_artists = %s WHERE exhib_id = %s""",
         (exhib_at, exhib_price, exhib_gallery, exhib_title, exhib_curator, exhibition_artists, exhibition_id))
        conn.commit()
        print("Exhibition updated successfully!")
    except Exception as e:
        print("An error occurred while updating the exhibition:", e)
   
def delete_exhibit(cur, conn, exhib_id):
    try:
        cur.execute("DELETE FROM exhibitions WHERE exhib_id = %s", (exhib_id,))
        conn.commit()
        print("Exhibit deleted successfully")
    except Exception as e:
        print("An error occurred while deleting the exhibit", e)

'''def insert_exhib_ticket_transaction(cur, conn, exhib_name, num_tickets, email):
    try:
        # Generate a unique transaction ID
        event_transac_id = uuid.uuid4()

        # Get the user ID for the given email address
        cur.execute("""SELECT user_id FROM user_account WHERE email = %s""", (email,))
        user_id = cur.fetchone()[0]

        # Get the exhibition ID for the given exhibition name
        cur.execute("""SELECT exhib_id FROM exhibitions WHERE exhib_name = %s""", (exhib_name,))
        event_id = cur.fetchone()[0]

        # Insert the ticket transaction into the database
        cur.execute("""INSERT INTO ticket_sales
                        VALUES (%s, %s, %s, %s, %s)""",
                    (event_transac_id, user_id, event_id, exhib_name, num_tickets))
        conn.commit()

        # Print a success message to the command line
        print("Ticket transaction inserted successfully")
    except Exception as e:
        print("An error occurred while inserting the transaction:", e)'''