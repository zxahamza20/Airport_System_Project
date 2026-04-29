import mysql.connector
from mysql.connector import Error

DB_CONFIG = { 
    "host": "localhost",
    'user': 'root',
    'password': '',
    'database': 'airline_db',
    'autocommit': True
}

def connect_to_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    
def get_cursor(conn):
    return conn.cursor(dictionary=True)

def close_connection(conn):
    if conn and conn.is_connected():
        conn.close()