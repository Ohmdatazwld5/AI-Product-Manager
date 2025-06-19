import sqlite3

def init_feedback_db():
    with sqlite3.connect("feedback.db") as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY,
            prompt TEXT,
            response TEXT,
            rating INTEGER
        )
        """)

def store_feedback(prompt: str, response: str, rating: int):
    with sqlite3.connect("feedback.db") as conn:
        conn.execute(
            "INSERT INTO feedback (prompt, response, rating) VALUES (?, ?, ?)",
            (prompt, response, rating)
        )