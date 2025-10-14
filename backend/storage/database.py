import sqlite3

def get_connection():
    conn = sqlite3.connect("data/sks.db")
    return conn