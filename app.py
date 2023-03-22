from flask import Flask, render_template, request, redirect, url_for

import psycopg2

app = Flask(__name__)


# establish a connection to the database
conn = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="myusername",
    password="mypassword"
)


@app.route('/add_artwork', methods=['GET', 'POST'])
def add_artwork():
    if request.method == 'POST':
        # process form data and add new artwork to the database
        object_number = request.form['object_number']
        artwork_title = request.form['artwork_title']
        artist = request.form['artist']
        culture = request.form['culture']
        made_on = request.form['made_on']
        object_type = request.form['object_type']
        art_department = request.form['art_department']
        dimensions = request.form['dimensions']
        
        # insert the new artwork into the database
        with conn:
            with conn.cursor() as cur:
                cur.execute('''INSERT INTO artwork (object_number, artwork_title, artist, culture, made_on, object_type, art_department, dimensions)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', 
                            (object_number, artwork_title, artist, culture, made_on, object_type, art_department, dimensions))
        
        # redirect to the artworks page
        return redirect(url_for('artworks'))
        
    else:
        # display the data entry form
        return render_template('add_artwork.html')


@app.route('/artworks')
def artworks():
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM artwork")
            artworks = cur.fetchall()
            
    return render_template('artworks.html', artworks=artworks)

