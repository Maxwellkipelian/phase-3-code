# database/connection.py
import sqlite3

def get_connection():
    conn = sqlite3.connect('database.db')
    return conn