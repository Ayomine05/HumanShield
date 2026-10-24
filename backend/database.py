import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "humanshield.db")


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            sub TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            last_score INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id TEXT NOT NULL,
            scenario_id TEXT NOT NULL,
            score INTEGER NOT NULL,
            completed_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skill_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_id TEXT NOT NULL,
            safe INTEGER NOT NULL,
            completed_at TEXT NOT NULL
        )
    """)

    existing = cursor.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
    if existing == 0:
        seed_categories(cursor)

    conn.commit()
    conn.close()


def seed_categories(cursor):
    starter_data = [
        ("education", "Education", "Fake scholarships, admissions, exam results", "Intermediate", 71),
        ("finance", "Finance", "Fake bank reps, OTP requests, loans, investments", "Advanced", 48),
        ("work", "Work", "Fake managers, HR, IT support, BEC", "Intermediate", 63),
        ("economy", "Economy", "Fake grants, relief funds, job offers", "Beginner", None),
        ("social", "Social Media", "Fake support, verification requests, giveaways", "Intermediate", 82),
        ("shopping", "Shopping & E-commerce", "Fake stores, deliveries, refunds", "Beginner", 77),
        ("personal", "Personal & Relationships", "Romance scams, fake emergencies", "Advanced", 39),
        ("government", "Government & Public Services", "Fake officials, tax, immigration", "Intermediate", None),
        ("gaming", "Gaming & Entertainment", "Fake rewards, account recovery, currency", "Beginner", 90),
    ]

    cursor.executemany(
        "INSERT INTO categories (id, name, sub, difficulty, last_score) VALUES (?, ?, ?, ?, ?)",
        starter_data
    )