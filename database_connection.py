from flask import Flask
import psycopg2
import template

app = Flask(__name__)

# Connect to PostgreSQL database
try:
    conn = psycopg2.connect(
        host="team8.postgres.database.azure.com",
        database="postgres",
        user="team8",
        password="server1234!"
    )
    print("Good connection")
except:
    print("Unable to connect to the database")