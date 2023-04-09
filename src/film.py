# import
import uuid

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

def insert_film_sales(cur, film_transac_id, user_id, film_id, film_transac_at):
    try:
        cur.execute("""INSERT INTO film_ticket_sales VALUES (%s, %s, %s, %s, %s)""", (film_transac_id, user_id, film_id, film_transac_at))
    except Exception as e:
        print("An error occurred while inserting the film sales record:", e)

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
