# report functions
def insert_gift_rep(cur, g_name, s_date, e_date):
    cur.execute("""
    SELECT i.gift_sku, i.gift_name, i.gift_price, DATE(s.gift_transaction_at)
    FROM gift_shop_item as i
    INNER JOIN gift_shop_sales as s 
    ON s.gift_sku = i.gift_sku 
    WHERE i.gift_name = %s AND DATE(s.gift_transaction_at) >= %s AND DATE(s.gift_transaction_at) <= %s """, [g_name, s_date, e_date]
    )
    data = cur.fetchall() #TODO: test if need to insert data?
    return data
'''
def insert_ticket_rep(cur, s_date,e_date, num_tickets):
    cur.execute("""
        SELECT exhib_title as event, exhib_ticket_price as ticket_price, DATE(exhib_transac_at), SUM (num_tickets) as et_total
        FROM exhibitions as e, 
            INNER JOIN exhib_ticket_sales as et ON e.exhib_id = et.exhib_id
        WHERE e.exhib_title = %s AND DATE(exhib_transac_at) >= %s AND DATE(exhib_transac_at) <= %s
        UNION
        SELECT film_title, film_ticket_price, DATE(film_transac_at), SUM(num_tickets) as ft_total
        FROM films as f
            INNER JOIN film_ticket_sales as ft ON f.film_id = ft.film_id
        WHERE f.film_title = %s AND DATE(film_transac_at) >= %s AND DATE(film_transac_at) <= %s
        """, [s_date, e_date, s_date,e_date, num_tickets]
        )
    data = cur.fetchall()
    return data

'''
