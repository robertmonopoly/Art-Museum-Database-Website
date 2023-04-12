from flask import Flask, flash

def retrieve_member_data(cur):
    cur.execute("""SELECT * FROM user_account""")
    data = cur.fetchall()
    return data    

def update_member(cur, conn, email, membership_type):
    try:
        cur.execute("UPDATE user_account SET membership = %s WHERE email = %s", 
            (membership_type, email))
        conn.commit()
        
        if membership_type == 'BASIC':
            amount_charged = 20
        elif membership_type == 'SILVER':
            amount_charged = 30
        elif membership_type == 'GOLD':
            amount_charged = 40
        message = f"The following amount has been charged to your account: ${amount_charged}"
        
        flash(message, 'success')
        return redirect(url_for('members'))
        
    except Exception as e:
        print("An error occurred while updating the user account: ", e)


        
        print("User membership status updated successfully")
        return render_template('members.html', message=message)
    except Exception as e:
        print("An error occurred while updating the user account: ", e)


def delete_member(cur, conn, user_account_id):
    try:
        cur.execute("UPDATE user_account SET account_status = %s WHERE user_id = %s", 
            (0, user_account_id))
        conn.commit()
        print("User account deleted successfully")
    except Exception as e:
        print("An error occurred while deleting the user account: ", e)
