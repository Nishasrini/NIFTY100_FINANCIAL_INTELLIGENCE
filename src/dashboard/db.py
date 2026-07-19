import sqlite3

DB_PATH = "data/nifty100.db"

def get_connection():
    return sqlite3.connect(DB_PATH)