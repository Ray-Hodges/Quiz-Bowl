# database.py

import sqlite3

DB_NAME = "quiz_data.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    courses = ["DS_3850", "DS_3860", "FIN_3210", "DS_4125", "PSY_1030"]
    for course in courses:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {course} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                option_a TEXT,
                option_b TEXT,
                option_c TEXT,
                option_d TEXT,
                correct_answer TEXT
            )
        """)

    conn.commit()
    conn.close()
