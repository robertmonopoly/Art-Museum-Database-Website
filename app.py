from flask import Flask
import psycopg2
import database_connection


app = Flask(__name__)

# Connect to PostgreSQL database

# The "cur" input variable comes from:
# con = psycopg2.connect("host="",
#     database="",
#     user="",
#     password="")
# cur = con.cursor()
# print("Connected to Postgres")

database_connection.connect_to_database()