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
   

def insert_exhib_sales(cur, exhib_transac_id, user_id, exhib_id, exhib_transac_at):
    try:
        cur.execute("""INSERT INTO exhibition_ticket_sales VALUES(%s, %s, %s, %s)""", (exhib_transac_id, user_id, exhib_id, exhib_transac_at))
    except Exception as e:
        print("An error occurred while inserting the exhibition sales record:", e)

def delete_exhibit(cur, conn, exhib_id):
    try:
        cur.execute("DELETE FROM exhibitions WHERE exhib_id = %s", (exhib_id,))
        conn.commit()
        print("Exhibit deleted successfully")
    except Exception as e:
        print("An error occurred while deleting the exhibit", e)

