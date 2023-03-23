from flask import Flask
import psycopg2
import database_connection


app = Flask(__name__)

# Connect to PostgreSQL database

database_connection.connect_to_database()