import sqlite3
import os
from datetime import datetime

DB_PATH = "data/attendance.db"

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (person_id) REFERENCES people (id)
        )
    """)

    conn.commit()
    conn.close()

def get_or_create_person(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM people WHERE name = ?", (name,))
    row = cursor.fetchone()

    if row:
        person_id = row[0]
    else:
        cursor.execute("INSERT INTO people (name) VALUES (?)", (name,))
        person_id = cursor.lastrowid
        conn.commit()

    conn.close()
    return person_id

def log_attendance(name):
    person_id = get_or_create_person(name)
    timestamp = datetime.now().isoformat()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO attendance_log (person_id, timestamp) VALUES (?, ?)",
        (person_id, timestamp)
    )
    conn.commit()
    conn.close()
    print(f"Logged attendance: {name} at {timestamp}")

def get_all_logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT people.name, attendance_log.timestamp
        FROM attendance_log
        JOIN people ON attendance_log.person_id = people.id
        ORDER BY attendance_log.timestamp DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    print("Database initialized at", DB_PATH)