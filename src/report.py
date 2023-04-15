# report functions
def insert_gift_rep(cur, g_name, s_date, e_date):
    cur.execute("""
    SELECT i.gift_sku, i.gift_name, i.gift_price, DATE(s.gift_transaction_at)
    FROM gift_shop_item as i
    INNER JOIN gift_shop_sales as s 
    ON s.gift_sku = i.gift_sku 
    WHERE i.gift_name = %s AND DATE(s.gift_transaction_at) >= %s AND DATE(s.gift_transaction_at) <= %s """, [g_name, s_date, e_date]
    )
    data = cur.fetchall()
    return data



#2rd report 
def insert_ticket_rep(cur, s_date,e_date):
    cur.execute("""
        SELECT exhib_title as event, exhib_ticket_price as ticket_price, DATE(ets.transact_at)
        FROM exhibitions as e
        INNER JOIN ticket_sales as ets
        ON ets.event_id = e.exhib_id 
        WHERE DATE(ets.transact_at) >= %s AND DATE(ets.transact_at) <= %s
        UNION
        SELECT film_title, film_ticket_price, DATE(fts.transact_at)
        FROM films as f
        INNER JOIN ticket_sales as fts
        ON fts.event_id = f.film_id 
        WHERE DATE(fts.transact_at) >= %s AND DATE(fts.transact_at) <= %s
        """, [s_date, e_date, s_date,e_date]
        )
    data = cur.fetchall()
    return data

def get_ticket_sales_sum(cur, s_date, e_date):
    cur.execute("""SELECT SUM(num_tickets)
    FROM ticket_sales as ts
    WHERE DATE(ts.transact_at) >= %s AND DATE(ts.transact_at) <= %s
    """, (s_date, e_date))
    # TODO: need to test
    sum_tickets = cur.fetchone()
    cur.execute("""SELECT SUM(user_price)
    FROM ticket_sales as ts
    WHERE DATE(ts.transact_at) >= %s AND DATE(ts.transact_at) <= %s""")
    sum_price = cur.fetchone()
    # returns tuple of both data
    return (sum_tickets, sum_price)

