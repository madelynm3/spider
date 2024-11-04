# database/db_manager.py
import sqlite3
from config import CONFIG

def setup_database():
    conn = sqlite3.connect(CONFIG['database'])
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reviews (...)''')
    conn.commit()
    return conn

def store_reviews(reviews):
    conn = setup_database()
    cursor = conn.cursor()
    # Insert reviews into the database
    conn.commit()
    conn.close()
