# db.py
import mysql.connector

def get_db_connection():
    """Establish and return a connection to the MySQL database."""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",         # Change this to your MySQL user
        password="Rajesha@1234", # Change this to your MySQL password
        database="bakery_management"
    )
    return connection
