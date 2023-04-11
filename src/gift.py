# imports
import uuid 

def insert_gift_item(cur, conn, gift_name, gift_type, gift_price):
    try:
        # Generate a unique transaction ID using the uuid4() function
        gift_sku = str(uuid.uuid4())
        sql_query = """INSERT INTO gift_shop_item VALUES (%s, %s, %s, %s)"""
        values = (gift_sku, gift_name, gift_type, gift_price)
        cur.execute(sql_query,values)
        conn.commit()
        print("Gift item inserted successfully.") 
    except Exception as e:
        print (f"Error inserting gift item: {e}")
   
def update_gift_item(cur, conn, gift_sku, gift_name, gift_type, gift_price):
    sql_query = """UPDATE gift_shop_item SET gift_name = %s, gift_type = %s, gift_price = %s WHERE gift_SKU = %s"""
    values = (gift_name, gift_type, gift_price, gift_sku)
    try:
        cur.execute(sql_query,values)
        conn.commit()
        print("Gift item updated successfully.")
    except Exception as e:
        print (f"Error updating gift item: {e}")

def delete_gift_shop_item(cur, conn, gift_sku):
    try:
        cur.execute("DELETE FROM gift_shop_item WHERE gift_sku = %s", (gift_sku,))
        conn.commit()
        print("Item deleted successfully")
    except Exception as e:
        print("An error occurred while deleting the item", e)

def insert_gift_sales(cur, transac_id, gift_sku, transac_at, user_id):
    # Generate a unique transaction ID using the uuid4() function
    transac_id = str(uuid.uuid4())
    sql = "INSERT INTO gift_shop_sales VALUES (%s, %s, %s, %s)"
    try:
        cur.execute(sql, (transac_id, gift_sku, transac_at, user_id))
        cur.commit()
        print("Gift sales inserted successfully!")   
    except Exception as e:
        print(f"Error inserting values into gift table: {e}")

